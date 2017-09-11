from azure.storage.blob import PublicAccess
from azure.storage import CloudStorageAccount
from azure.storage.blob import (
    ContentSettings,
    BlobBlock,
    BlockListType,
)
import uuid
import datetime

class LogoStorageConnector:
	def __init__(self):
		try:
			import config as config
			self.config = config
		except:
			raise ValueError('Please specify configuration settings in config.py.')
		self.account = CloudStorageAccount(account_name=config.STORAGE_ACCOUNT_NAME, account_key=config.STORAGE_ACCOUNT_KEY)
		self.service = self.account.create_block_blob_service()
		self._create_input_container()
		self._create_output_container()

	""" Public Interfaces """
	""" Upload """
	def upload_brand_training_input_data(self, brand, data):
		container = self._input_container()
		path = '{}/{}'.format(brand, self.config.TRAINING_DIRECTORY_NAME)
		self._upload_data(container, path, data)

	def upload_brand_operational_input_data(self, brand, data):
		container = self._input_container()
		path = '{}/{}'.format(brand, self.config.OPERATIONAL_DIRECTORY_NAME)
		self._upload_data(container, path, data)

	def upload_brand_operational_output_data(self, brand, data):
		container = self._output_container()
		path = '{}/{}'.format(brand, self.config.OPERATIONAL_DIRECTORY_NAME)
		self._upload_data(container, path, data)

	""" Download """
	def download_brand_training_input_data(self, brand):
		path = '{}/{}'.format(brand, self.config.TRAINING_DIRECTORY_NAME)
		blobs = self.service.list_blobs(container_name=self.config.INPUT_CONTAINER_NAME, prefix=path)
		return blobs

	def download_brand_operational_input_data(self, brand):
		path = '{}/{}'.format(brand, self.config.OPERATIONAL_DIRECTORY_NAME)
		blobs = self.service.list_blobs(container_name=self.config.INPUT_CONTAINER_NAME, prefix=path)
		return blobs

	def download_brand_operational_output_data(self, brand):
		path = '{}/{}'.format(brand, self.config.OPERATIONAL_DIRECTORY_NAME)
		blobs = self.service.list_blobs(container_name=self.config.OUTPUT_CONTAINER_NAME, prefix=path)
		return blobs
		
	""" Pretty Print """

	def pretty_print_storage_structure(self):
		containers = self.service.list_containers()
		for container in containers:
			self.pretty_print_container_contents(container.name)

	def pretty_print_container_contents(self, container_name):
		print(container_name)
		blobs = self.service.list_blobs(self.config.INPUT_CONTAINER_NAME)
		for blob in blobs:
			print ('	{}'.format(blob.name))

	""" Private """

	def _create_input_container(self):
		self.service.create_container(self.config.INPUT_CONTAINER_NAME)

	def _create_output_container(self):
		self.service.create_container(self.config.OUTPUT_CONTAINER_NAME)

	def _input_container(self):
		return self.config.INPUT_CONTAINER_NAME

	def _output_container(self):
		return self.config.OUTPUT_CONTAINER_NAME

	def _get_resource_reference(self, prefix):
		return '{}/{}=={}'.format(prefix, str(uuid.uuid4())[:8], datetime.datetime.now().strftime("%m-%d-%Y %I:%M%p"))

	def _get_blob_reference(self, prefix='blob'):
		return self._get_resource_reference(prefix)

	def _upload_data(self, container_name, path, data):
		blob_name = self._get_blob_reference(path);
		self.service.create_blob_from_text(container_name, blob_name, data)
		return blob_name

	def _download_data(self, container_name, full_blob_name):
		blob = self.service.get_blob_to_text(container_name, blob_name)
		content = blob.content
		return content
