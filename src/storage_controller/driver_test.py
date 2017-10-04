from ig_proccessing_driver import IGProccessingDriver
from table_manager import TableStorageConnector

test_driver = False
test_tables = False
if(test_driver == True):
	driver = IGProccessingDriver()
	driver.start_processing()

if(test_tables == True):
	table_manager = TableStorageConnector()
	table_manager.get_all_entries('patagonia')

