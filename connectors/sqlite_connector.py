import pandas as pd
import sqlite3 as sqlite

from connectors.base_connector import BaseConnector


class SQLiteConnector(BaseConnector):

    def __init__(self, source):

        self.source = source
        self.connection = None

    def connect(self):
        """
        Establish SQLite connection.
        """
        self.connection = sqlite.connect(self.source)


    def collect(
    self,
    query: str = None,
    table: str = None
    ) -> pd.DataFrame:

        """
        Load data from a SQLite database.

        Parameters:
            query:
                Optional SQL query to execute.

            table:
                Optional table name to load.

        Behavior:
            - If query is provided, execute the query.
            - If table is provided, load that table.
            - If neither is provided, discover available tables.
        """

        # ---------------------------------------------------------
        # CASE 1: SQL QUERY PROVIDED
        # ---------------------------------------------------------

        if query is not None:

            return pd.read_sql_query(
                query,
                self.connection
            )


        # ---------------------------------------------------------
        # CASE 2: TABLE NAME PROVIDED
        # ---------------------------------------------------------

        if table is not None:

            query = f'''
                SELECT *
                FROM "{table}"
            '''

            return pd.read_sql_query(
                query,
                self.connection
            )


        # ---------------------------------------------------------
        # CASE 3: NO QUERY OR TABLE PROVIDED
        # ---------------------------------------------------------

        tables = pd.read_sql_query(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
            """,
            self.connection
        )

        if tables.empty:

            raise ValueError(
                "No tables found in SQLite database."
            )


        # Display available tables

        print("\nAvailable SQLite tables:")
        print("------------------------")

        for index, table_name in enumerate(
            tables["name"],
            start=1
        ):
            print(
                f"{index}. {table_name}"
            )


        # Ask user to select table

        selection = input(
            "\nSelect a table number: "
        )


        try:

            selection = int(selection)

        except ValueError:

            raise ValueError(
                "Table selection must be a number."
            )


        if selection < 1 or selection > len(tables):

            raise ValueError(
                "Invalid table selection."
            )


        table_name = tables.iloc[
            selection - 1
        ]["name"]


        query = f'''
            SELECT *
            FROM "{table_name}"
        '''


        return pd.read_sql_query(
            query,
            self.connection
        )

    def close(self):

        if self.connection:
            self.connection.close()
