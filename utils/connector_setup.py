from utils.registry import ConnectorRegistry
from connectors.csv_connector import CSVConnector
from connectors.excel_connector import ExcelConnector


def create_registry():

    registry = ConnectorRegistry()

    registry.register(".csv", CSVConnector)
    registry.register(".xlsx", ExcelConnector)

    return registry