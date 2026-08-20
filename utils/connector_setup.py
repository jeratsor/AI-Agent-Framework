from utils.registry import ConnectorRegistry
from connectors.csv_connector import CSVConnector
from connectors.excel_connector import ExcelConnector
from connectors.api_connector import RESTAPIConnector
from connectors.sqlite_connector import SQLiteConnector
from connectors.sharepoint_connector import SharePointConnector


def create_registry():

    registry = ConnectorRegistry()

    registry.register(".csv", CSVConnector)
    registry.register(".xlsx", ExcelConnector)
    registry.register("api", RESTAPIConnector)
    registry.register(".db", SQLiteConnector)
    registry.register("sharepoint", SharePointConnector)

    return registry