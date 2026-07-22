"""
Base connector for all data sources.

Every connector returns a pandas DataFrame.
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseConnector(ABC):
    """
    Abstract connector class.
    """

    def __init__(self, source: str):
        self.source = source

    @abstractmethod
    def connect(self):
        """Optional setup before collecting."""
        pass

    @abstractmethod
    def collect(self) -> pd.DataFrame:
        """
        Returns a pandas DataFrame.
        """
        pass

    @abstractmethod
    def close(self):
        """Close any connections."""
        pass