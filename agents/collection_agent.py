from pathlib import Path
import pandas as pd

from agents.base_agent import BaseAgent
from connectors.csv_connector import CSVConnector


class CollectionAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="Collection Agent",
            description="Collects data from multiple sources."
        )

    def execute(self):
        """
        Required by BaseAgent.

        For now this simply returns True.
        """
        return True

    def collect(self, source: str) -> pd.DataFrame:

        extension = Path(source).suffix.lower()

        if extension == ".csv":

            connector = CSVConnector(source)

        else:

            raise ValueError(
                f"No connector available for {extension}"
            )

        self.logger.info(f"Collecting data from {source}")

        df = connector.collect()

        self.update_metric("rows", len(df))

        self.update_metric("columns", len(df.columns))

        self.logger.info(
            f"Collected {len(df)} rows."
        )

        return df