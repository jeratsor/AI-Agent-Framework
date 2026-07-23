

from utils.registry import ConnectorRegistry
from connectors.csv_connector import CSVConnector
from connectors.excel_connector import ExcelConnector
from utils.connector_setup import create_registry


registry = create_registry()


print(registry.available_connectors())


connector = registry.get_connector(
    "data/sales.xlsx"
)

connector.connect()

data = connector.collect()

connector.close()

print(data)