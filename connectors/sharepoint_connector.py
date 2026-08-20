import os
import sqlite3
import tempfile
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

import msal
import pandas as pd
import requests

from dotenv import load_dotenv

from connectors.base_connector import BaseConnector


load_dotenv()


class SharePointConnector(BaseConnector):

    GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

    def __init__(self, source: str):

        self.source = source

        # =========================================================
        # MICROSOFT ENTRA / GRAPH CREDENTIALS
        # =========================================================

        self.tenant_id = os.getenv(
            "SHAREPOINT_TENANT_ID"
        )

        self.client_id = os.getenv(
            "SHAREPOINT_CLIENT_ID"
        )

        self.client_secret = os.getenv(
            "SHAREPOINT_CLIENT_SECRET"
        )

        # =========================================================
        # SHAREPOINT SITE
        #
        # Example:
        #
        # https://jaja626returns.sharepoint.com/
        #
        # or:
        #
        # https://jaja626returns.sharepoint.com/sites/Finance
        # =========================================================

        self.site_url = os.getenv(
            "SHAREPOINT_SITE_URL"
        )

        # =========================================================
        # OPTIONAL DOCUMENT LIBRARY
        #
        # Example:
        #
        # SHAREPOINT_DRIVE_NAME=Documents
        #
        # If omitted, the connector will automatically select:
        #
        # 1. Documents
        # 2. First available document library
        # =========================================================

        self.drive_name = os.getenv(
            "SHAREPOINT_DRIVE_NAME"
        )

        # =========================================================
        # RUNTIME VALUES
        #
        # These are discovered when connect() runs.
        # =========================================================

        self.access_token = None

        self.site_id = None
        self.drive_id = None

        self.site_name = None
        self.drive_display_name = None


    # =============================================================
    # CONNECT
    # =============================================================

    def connect(self):

        # ---------------------------------------------------------
        # Validate configuration
        # ---------------------------------------------------------

        required_settings = {
            "SHAREPOINT_TENANT_ID": self.tenant_id,
            "SHAREPOINT_CLIENT_ID": self.client_id,
            "SHAREPOINT_CLIENT_SECRET": self.client_secret,
            "SHAREPOINT_SITE_URL": self.site_url
        }

        missing = [
            name
            for name, value in required_settings.items()
            if not value
        ]

        if missing:

            raise RuntimeError(
                "Missing SharePoint configuration: "
                + ", ".join(missing)
            )


        # ---------------------------------------------------------
        # Authenticate with Microsoft Entra ID
        # ---------------------------------------------------------

        authority = (
            "https://login.microsoftonline.com/"
            f"{self.tenant_id}"
        )

        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret
        )

        result = app.acquire_token_for_client(
            scopes=[
                "https://graph.microsoft.com/.default"
            ]
        )

        if "access_token" not in result:

            error_description = result.get(
                "error_description",
                "Unknown authentication error."
            )

            raise RuntimeError(
                "Microsoft Graph authentication failed.\n"
                f"Details: {error_description}"
            )

        self.access_token = result[
            "access_token"
        ]


        # ---------------------------------------------------------
        # Graph headers
        # ---------------------------------------------------------

        headers = {
            "Authorization":
                f"Bearer {self.access_token}"
        }


        # ---------------------------------------------------------
        # Parse SharePoint URL
        # ---------------------------------------------------------

        hostname, relative_path = (
            self._parse_site_url(
                self.site_url
            )
        )


        # ---------------------------------------------------------
        # Discover SharePoint site
        #
        # Root site:
        #
        # https://tenant.sharepoint.com/
        #
        # Graph:
        #
        # /sites/{hostname}
        #
        # Subsite:
        #
        # https://tenant.sharepoint.com/sites/Finance
        #
        # Graph:
        #
        # /sites/{hostname}:/sites/Finance
        # ---------------------------------------------------------

        if relative_path == "/":

            graph_url = (
                f"{self.GRAPH_BASE_URL}"
                f"/sites/{hostname}"
            )

        else:

            graph_url = (
                f"{self.GRAPH_BASE_URL}"
                f"/sites/{hostname}:"
                f"{relative_path}"
            )


        response = requests.get(
            graph_url,
            headers=headers
        )


        if not response.ok:

            raise RuntimeError(
                "Could not find SharePoint site.\n"
                f"Configured URL: {self.site_url}\n"
                f"Graph endpoint: {graph_url}\n"
                f"Status: {response.status_code}\n"
                f"Response: {response.text}"
            )


        site_info = response.json()


        self.site_id = site_info.get(
            "id"
        )

        self.site_name = site_info.get(
            "displayName"
        )


        if not self.site_id:

            raise RuntimeError(
                "Microsoft Graph returned the SharePoint "
                "site, but no site ID was provided."
            )


        # ---------------------------------------------------------
        # Discover document libraries
        # ---------------------------------------------------------

        drives_url = (
            f"{self.GRAPH_BASE_URL}"
            f"/sites/{self.site_id}/drives"
        )


        response = requests.get(
            drives_url,
            headers=headers
        )


        if not response.ok:

            raise RuntimeError(
                "SharePoint site was found, but its "
                "document libraries could not be discovered.\n"
                f"Site: {self.site_name}\n"
                f"Status: {response.status_code}\n"
                f"Response: {response.text}"
            )


        drives = response.json().get(
            "value",
            []
        )


        if not drives:

            raise RuntimeError(
                f"No document libraries were found "
                f"for SharePoint site '{self.site_name}'."
            )


        # ---------------------------------------------------------
        # Select document library
        # ---------------------------------------------------------

        selected_drive = None


        # ---------------------------------------------------------
        # Explicit drive name from .env
        # ---------------------------------------------------------

        if self.drive_name:

            for drive in drives:

                if (
                    drive.get("name", "").lower()
                    == self.drive_name.lower()
                ):

                    selected_drive = drive
                    break


            if selected_drive is None:

                available_drives = [
                    drive.get("name")
                    for drive in drives
                ]

                raise RuntimeError(
                    f"SharePoint document library "
                    f"'{self.drive_name}' was not found.\n"
                    f"Available libraries: "
                    f"{available_drives}"
                )


        # ---------------------------------------------------------
        # Automatic drive selection
        # ---------------------------------------------------------

        else:

            # Prefer Documents

            for drive in drives:

                if (
                    drive.get("name", "").lower()
                    == "documents"
                ):

                    selected_drive = drive
                    break


            # Otherwise use first available library

            if selected_drive is None:

                selected_drive = drives[0]


        # ---------------------------------------------------------
        # Store selected drive information
        # ---------------------------------------------------------

        self.drive_id = selected_drive.get(
            "id"
        )

        self.drive_display_name = selected_drive.get(
            "name"
        )


        if not self.drive_id:

            raise RuntimeError(
                "A SharePoint document library was "
                "discovered, but it has no drive ID."
            )


    # =============================================================
    # PARSE SHAREPOINT SITE URL
    # =============================================================

    def _parse_site_url(
        self,
        site_url: str
    ):

        parsed = urlparse(
            site_url
        )


        if parsed.scheme not in (
            "http",
            "https"
        ):

            raise ValueError(
                "SHAREPOINT_SITE_URL must be a valid "
                "HTTP or HTTPS URL."
            )


        hostname = parsed.netloc


        if not hostname:

            raise ValueError(
                "SHAREPOINT_SITE_URL does not contain "
                "a valid SharePoint hostname."
            )


        relative_path = (
            parsed.path
            or "/"
        )


        # Remove trailing slash from non-root sites

        if (
            relative_path != "/"
            and relative_path.endswith("/")
        ):

            relative_path = (
                relative_path.rstrip("/")
            )


        return hostname, relative_path


    # =============================================================
    # COLLECT
    # =============================================================

    def collect(
        self,
        file_path: str
    ) -> pd.DataFrame:

        # ---------------------------------------------------------
        # Validate connection
        # ---------------------------------------------------------

        if not self.access_token:

            raise RuntimeError(
                "Connector is not connected. "
                "Call connect() first."
            )


        if not self.drive_id:

            raise RuntimeError(
                "SharePoint document library has not "
                "been discovered."
            )


        if not file_path:

            raise ValueError(
                "file_path cannot be empty."
            )


        # ---------------------------------------------------------
        # Graph headers
        # ---------------------------------------------------------

        headers = {
            "Authorization":
                f"Bearer {self.access_token}"
        }


        # ---------------------------------------------------------
        # Normalize file path
        # ---------------------------------------------------------

        file_path = file_path.strip()

        file_path = file_path.lstrip("/")


        # ---------------------------------------------------------
        # Find file in SharePoint
        # ---------------------------------------------------------

        encoded_path = requests.utils.quote(
            file_path,
            safe="/"
        )


        graph_url = (
            f"{self.GRAPH_BASE_URL}"
            f"/drives/{self.drive_id}"
            f"/root:/{encoded_path}"
        )


        response = requests.get(
            graph_url,
            headers=headers
        )


        if not response.ok:

            raise RuntimeError(
                "Could not find SharePoint file.\n"
                f"File: {file_path}\n"
                f"Library: {self.drive_display_name}\n"
                f"Status: {response.status_code}\n"
                f"Response: {response.text}"
            )


        file_info = response.json()


        file_id = file_info.get(
            "id"
        )


        if not file_id:

            raise RuntimeError(
                "SharePoint returned file information "
                "but no file ID was provided."
            )


        # ---------------------------------------------------------
        # Download file
        # ---------------------------------------------------------

        download_url = (
            f"{self.GRAPH_BASE_URL}"
            f"/drives/{self.drive_id}"
            f"/items/{file_id}/content"
        )


        response = requests.get(
            download_url,
            headers=headers
        )


        if not response.ok:

            raise RuntimeError(
                "SharePoint file was found, but could "
                "not be downloaded.\n"
                f"File: {file_path}\n"
                f"Status: {response.status_code}\n"
                f"Response: {response.text}"
            )


        file_bytes = BytesIO(
            response.content
        )


        # ---------------------------------------------------------
        # Determine file extension
        # ---------------------------------------------------------

        extension = Path(
            file_path
        ).suffix.lower()


        # =========================================================
        # EXCEL
        # =========================================================

        if extension in (
            ".xlsx",
            ".xls"
        ):

            return pd.read_excel(
                file_bytes
            )


        # =========================================================
        # CSV
        # =========================================================

        elif extension == ".csv":

            return pd.read_csv(
                file_bytes
            )


        # =========================================================
        # SQLITE DATABASE
        # =========================================================

        elif extension == ".db":

            return self._read_sqlite_database(
                response.content,
                file_path
            )


        # =========================================================
        # UNSUPPORTED FILE TYPE
        # =========================================================

        else:

            raise ValueError(
                f"Unsupported SharePoint file type: "
                f"{extension}\n"
                "Supported formats: "
                ".xlsx, .xls, .csv, .db"
            )


    # =============================================================
    # READ SQLITE DATABASE
    # =============================================================

    def _read_sqlite_database(
        self,
        file_content: bytes,
        file_path: str
    ) -> pd.DataFrame:

        # ---------------------------------------------------------
        # Validate SQLite file signature
        #
        # A real SQLite database begins with:
        #
        # SQLite format 3
        # ---------------------------------------------------------

        sqlite_header = (
            b"SQLite format 3\x00"
        )


        if not file_content.startswith(
            sqlite_header
        ):

            raise ValueError(
                f"Downloaded SharePoint file "
                f"'{file_path}' does not appear to "
                "be a valid SQLite database.\n"
                "The downloaded content does not "
                "contain the SQLite file signature."
            )


        temp_db_path = None
        conn = None


        try:

            # -----------------------------------------------------
            # Create temporary .db file
            # -----------------------------------------------------

            with tempfile.NamedTemporaryFile(
                suffix=".db",
                delete=False
            ) as temp_file:

                temp_db_path = temp_file.name

                temp_file.write(
                    file_content
                )


            # -----------------------------------------------------
            # Open database
            # -----------------------------------------------------

            conn = sqlite3.connect(
                temp_db_path
            )


            cursor = conn.cursor()


            # -----------------------------------------------------
            # Find user tables
            # -----------------------------------------------------

            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name
                """
            )


            tables = [
                row[0]
                for row in cursor.fetchall()
            ]


            if not tables:

                raise ValueError(
                    f"SQLite database '{file_path}' "
                    "contains no user tables."
                )


            # -----------------------------------------------------
            # Select first table
            # -----------------------------------------------------

            table_name = tables[0]


            # -----------------------------------------------------
            # Log available tables
            # -----------------------------------------------------

            if hasattr(self, "logger"):

                self.logger.info(
                    f"SQLite tables found: {tables}"
                )

                self.logger.info(
                    f"Reading table: {table_name}"
                )


            # -----------------------------------------------------
            # Safely quote table name
            # -----------------------------------------------------

            quoted_table_name = (
                '"'
                + table_name.replace(
                    '"',
                    '""'
                )
                + '"'
            )


            # -----------------------------------------------------
            # Read table into DataFrame
            # -----------------------------------------------------

            df = pd.read_sql_query(
                f"SELECT * FROM "
                f"{quoted_table_name}",
                conn
            )


            return df


        except sqlite3.DatabaseError as e:

            raise RuntimeError(
                f"SQLite database '{file_path}' "
                f"could not be read.\n"
                f"SQLite error: {e}"
            ) from e


        finally:

            # -----------------------------------------------------
            # IMPORTANT:
            #
            # SQLite connection MUST be closed before Windows
            # allows the temporary file to be deleted.
            # -----------------------------------------------------

            if conn is not None:

                conn.close()

                conn = None


            # -----------------------------------------------------
            # Delete temporary database
            # -----------------------------------------------------

            if temp_db_path is not None:

                try:

                    if os.path.exists(
                        temp_db_path
                    ):

                        os.remove(
                            temp_db_path
                        )

                except PermissionError:

                    if hasattr(self, "logger"):

                        self.logger.warning(
                            "Could not immediately delete "
                            f"temporary SQLite file: "
                            f"{temp_db_path}"
                        )


    # =============================================================
    # CLOSE
    # =============================================================

    def close(self):

        self.access_token = None

        self.site_id = None

        self.drive_id = None

        self.site_name = None

        self.drive_display_name = None