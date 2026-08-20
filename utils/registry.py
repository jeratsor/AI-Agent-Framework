"""
registry.py

Connector Registry

Stores and retrieves connectors for the Collection Agent.
"""

from pathlib import Path


class ConnectorRegistry:
    """
    Registry for all available connectors.
    """

    def __init__(self):
        self._connectors = {}

    def register(self, extension: str, connector_class):
        """
        Register a connector.

        Example:
            registry.register(".csv", CSVConnector)
        """
        self._connectors[extension.lower()] = connector_class
       
                
    def get_connector(self, source: str):

        source_lower = source.lower()

        # Direct connector key - SharePoint, API, etc.
        if source_lower in self._connectors:

            connector_class = self._connectors[
                source_lower
            ]

            return connector_class(source)

        # -----------------------------------------
        # REST API URL
        # -----------------------------------------

        if source_lower.startswith(
            ("http://", "https://")
        ):

            if "api" in self._connectors:

                connector_class = self._connectors[
                    "api"
                ]

                return connector_class(source)

        # File extension - CSV, Excel, SQLite, etc.
        extension = Path(source).suffix.lower()

        if extension not in self._connectors:

            available = ", ".join(
                self._connectors.keys()
            )

            raise ValueError(
                f"No connector registered for '{extension}'. "
                f"Available connectors: {available}"
            )

        connector_class = self._connectors[
            extension
        ]

        return connector_class(source)

    def available_connectors(self):
        """
        Returns all registered connectors.
        """

        return list(self._connectors.keys())