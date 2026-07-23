

from utils.registry import ConnectorRegistry
from connectors.csv_connector import CSVConnector
from connectors.excel_connector import ExcelConnector


registry = ConnectorRegistry()

registry.register(".csv", CSVConnector)
registry.register(".xlsx", ExcelConnector)


print(registry.available_connectors())


connector = registry.get_connector(
    "data/sales.csv"
)

connector.connect()

data = connector.collect()

connector.close()

print(data)