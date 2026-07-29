import requests
import pandas as pd

from connectors.base_connector import BaseConnector


class RESTAPIConnector(BaseConnector):

    def __init__(self, source):

        self.source = source
        self.response = None


    def connect(self):
        """
        Establish API connection.
        """

        return True


    def collect(self):

        response = requests.get(
            self.source
        )

        response.raise_for_status()

        self.response = response.json()
        ## JSON returns a nested structure, so we need to normalize it into a flat table.
        return pd.json_normalize(self.response)

        return pd.DataFrame( self.response)
     
        """return pd.DataFrame( self.response)"""


    def close(self):

        self.response = None