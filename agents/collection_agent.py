from pathlib import Path
import pandas as pd

from agents.base_agent import BaseAgent
from connectors.csv_connector import CSVConnector
from utils.registry import ConnectorRegistry # main class with the connectors registry -acts as the intremediary to the connector and agent



class CollectionAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="Collection Agent",
            description="Collects data from multiple sources."
        )

        self.registry = ConnectorRegistry()
        self.registry.register(".csv", CSVConnector)
        #self.registry.register(".xlsx", ExcelConnector)


    def execute(self):
        """
        Required by BaseAgent.

        For now this simply returns True.
        """
        return True

    def collect(self, source: str) -> pd.DataFrame:

        extension = Path(source).suffix.lower()

        connector = self.registry.get_connector(source)

        self.logger.info(f"Collecting data from {source}")

        df = connector.collect()

        self.update_metric("rows", len(df))

        self.update_metric("columns", len(df.columns))

        self.logger.info(
            f"Collected {len(df)} rows."
        )

        return df