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
        Load Excel data without assuming a header row. 
        The HeaderDetector will be used later to determine the correct header.
        """
        self.data = pd.read_excel(self.source, header=None)

        return self.data

    def close(self):
        """
        Close connection.
        """
        self.data = None