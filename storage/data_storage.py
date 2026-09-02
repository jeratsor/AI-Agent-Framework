import sqlite3

import pandas as pd


class DataStorage:

    def __init__(self, database_path: str):
        self.database_path = database_path


    def save(
        self,
        df: pd.DataFrame,
        table_name: str,
        if_exists: str = "replace"
    ) -> None:
        """
        Save a DataFrame to a SQLite database.
        """

        if df.empty:
            raise ValueError(
                "Cannot save an empty DataFrame."
            )

        if not table_name:
            raise ValueError(
                "Table name cannot be empty."
            )

        connection = sqlite3.connect(
            self.database_path
        )

        try:

            df.to_sql(
                table_name,
                connection,
                if_exists=if_exists,
                index=False
            )

        finally:

            connection.close()


    def load(
        self,
        table_name: str
    ) -> pd.DataFrame:
        """
        Load a table from SQLite into a DataFrame.
        """

        if not table_name:
            raise ValueError(
                "Table name cannot be empty."
            )

        connection = sqlite3.connect(
            self.database_path
        )

        try:

            df = pd.read_sql_query(
                f'SELECT * FROM "{table_name}"',
                connection
            )

        finally:

            connection.close()

        return df


    def table_exists(
        self,
        table_name: str
    ) -> bool:
        """
        Check whether a table exists in the database.
        """

        connection = sqlite3.connect(
            self.database_path
        )

        try:

            query = """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name = ?
            """

            result = connection.execute(
                query,
                (table_name,)
            ).fetchone()

        finally:

            connection.close()

        return result is not None