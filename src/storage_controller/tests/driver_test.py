import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../..'))
# from src.Drivers.ig_proccessing_driver import IGProccessingDriver
from src.storage_controller.TableManagers.table_manager import TableStorageConnector
from src.storage_controller.Drivers.driver import Driver
from src.storage_controller.NetworkedFileSystem.nfs_controller_config import NFS_Controller_Config

test_old_driver = False
test_tables = False
test_new_driver = True
# if(test_old_driver == True):
# 	driver_old = IGProccessingDriver()
# 	driver_old.start_processing()

if(test_tables == True):
	table_manager = TableStorageConnector()
	table_manager.get_all_entries('patagonia')

# config = './nfs_test_config'
# config_path = os.path.abspath(input_config_name)
STORAGE_ACCOUNT_NAME = 'logodetectiontesting'
STORAGE_ACCOUNT_KEY = 'HF0EwhCG2R8BBeKGV5qrloyz5Ua0kYQlSQI/vDWsTv3AjjK2nDJOD6Y8iLPjtF6nMnJr2zQZ0xhxkDF0biCArg=='
config = NFS_Controller_Config(STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY)
if(test_new_driver == True):
	driver = Driver(config)
	driver.start_processing()
