import pandas as pd
import pandas as pd

from agents.base_agent import BaseAgent
from utils.connector_setup import create_registry


class CollectionAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="Collection Agent",
            description="Collects data from multiple sources."
        )

        # Pulls from the connector registry to get
        # the appropriate connector for the source type
        self.registry = create_registry()


    def execute(self):
        """
        Required by BaseAgent.
        """
        return True


    def collect(self, source: str, **kwargs) -> pd.DataFrame:

        self.logger.info(
            f"Collecting data from {source}"
        )

        connector = self.registry.get_connector(source)

        connector.connect()

        #Update to the collection agent so you can query SQL files from the collection agent.
        #df = connector.collect()
        try:
            df = connector.collect(**kwargs)
        finally:
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