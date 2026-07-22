import pandas as pd

from connectors.base_connector import BaseConnector


class CSVConnector(BaseConnector):
    """
    Reads CSV files.
    """

    def connect(self):
        # No connection required
        return True

    def collect(self) -> pd.DataFrame:

        self.connect()

        df = pd.read_csv(self.source)

        self.close()

        return df

    def close(self):
        return True