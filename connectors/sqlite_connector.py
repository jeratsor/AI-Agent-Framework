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


    def collect(self, query: str):

        """
        Load SQLite data.
        """

        #or 
        #connector = SQLiteConnector(
        #source="data/sample.db",
        #query= """
        #SELECT *
        #FROM employees
        #WHERE salary > 70000

        if query is None:
            query ="SELECT * FROM employees "
         #ELSE:   
        return pd.read_sql_query( query,self.connection)

        """return pd.DataFrame( self.response)"""

    def close(self):

        if self.connection:
            self.connection.close()
