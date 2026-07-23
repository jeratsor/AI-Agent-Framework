import pandas as pd

from connectors.base_connector import BaseConnector


class ExcelConnector(BaseConnector):

    # Collects data from Excel files (.xlsx)

    def __init__(self, source):
        self.source = source
        self.data = None

    def connect(self):
        """
        Establish connection to Excel file.
        """
        return True

    def collect(self):
        """
        Load Excel data.
        """
        self.data = pd.read_excel(self.source)
        return self.data

    def close(self):
        """
        Close connection.
        """
        self.data = None