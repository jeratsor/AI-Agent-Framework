import pandas as pd

from agents.base_agent import BaseAgent
from connectors.csv_connector import CSVConnector
from connectors.excel_connector import ExcelConnector
from utils.registry import ConnectorRegistry


class CollectionAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="Collection Agent",
            description="Collects data from multiple sources."
        )

        self.registry = ConnectorRegistry()

        self.registry.register(
            ".csv",
            CSVConnector
        )

        self.registry.register(
            ".xlsx",
            ExcelConnector
        )


    def execute(self):
        """
        Required by BaseAgent.
        """
        return True


    def collect(self, source: str) -> pd.DataFrame:

        self.logger.info(
            f"Collecting data from {source}"
        )

        connector = self.registry.get_connector(source)

        connector.connect()

        df = connector.collect()

        connector.close()


        self.update_metric(
            "rows",
            len(df)
        )

        self.update_metric(
            "columns",
            len(df.columns)
        )


        self.logger.info(
            f"Collected {len(df)} rows."
        )

        return df