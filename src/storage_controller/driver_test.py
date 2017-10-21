# from ig_proccessing_driver import IGProccessingDriver
from table_manager import TableStorageConnector
from driver import Driver

test_old_driver = False
test_tables = False
test_new_driver = True
# if(test_old_driver == True):
# 	driver_old = IGProccessingDriver()
# 	driver_old.start_processing()

if(test_tables == True):
	table_manager = TableStorageConnector()
	table_manager.get_all_entries('patagonia')

input_config_name = 'nfs_test_config'
if(test_new_driver == True):
	driver = Driver(input_config = input_config_name)
	driver.start_processing()
