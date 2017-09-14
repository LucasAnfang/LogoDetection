from azure.storage.blob import PublicAccess
from azure.storage import CloudStorageAccount
from azure.storage.blob import (
    ContentSettings,
    BlobBlock,
    BlockListType,
)
import uuid
import datetime
import json
from log_entries import *

class LogoStorageConnector:
	def __init__(self, Interacting_Entity = "Meh"):
		try:
			import config as config
			self.config = config
		except:
			raise ValueError('Please specify configuration settings in config.py.')
		try:
			import constants as constants
			self.constants = constants
		except:
			raise ValueError('Please specify networked file system contants in nfs_constants.py.')
		self.account = CloudStorageAccount(account_name=config.STORAGE_ACCOUNT_NAME, account_key=config.STORAGE_ACCOUNT_KEY)
		self.service = self.account.create_block_blob_service()
		self._create_input_container()
		self._create_output_container()
		self.Interacting_Entity = Interacting_Entity
		

	""" Public Interfaces """
	""" Upload """
	def upload_brand_training_input_data(self, brand, data):
		container = self._input_container()
		path = '{}/{}'.format(brand, self.constants.TRAINING_DIRECTORY_NAME)
		self._upload_data(container, path, data)

	def upload_brand_operational_input_data(self, brand, data):
		container = self._input_container()
		path = '{}/{}'.format(brand, self.constants.OPERATIONAL_DIRECTORY_NAME)
		self._upload_data(container, path, data)

	def upload_brand_operational_output_data(self, brand, data):
		container = self._output_container()
		path = '{}/{}'.format(brand, self.constants.OPERATIONAL_DIRECTORY_NAME)
		self._upload_data(container, path, data)

	""" Download """
	def download_brand_training_input_data(self, brand, action_filter):
		path = '{}/{}'.format(brand, self.constants.TRAINING_DIRECTORY_NAME)
		blobs = self.service.list_blobs(container_name=self.constants.INPUT_CONTAINER_NAME, prefix=path)
		return blobs

	def download_brand_operational_input_data(self, brand, action_filter):
		path = '{}/{}'.format(brand, self.constants.OPERATIONAL_DIRECTORY_NAME)
		blobs = self.service.list_blobs(container_name=self.constants.INPUT_CONTAINER_NAME, prefix=path)
		return blobs

	def download_brand_operational_output_data(self, brand):
		path = '{}/{}'.format(brand, self.constants.OPERATIONAL_DIRECTORY_NAME)
		blobs = self.service.list_blobs(container_name=self.constants.OUTPUT_CONTAINER_NAME, prefix=path)
		return blobs

	""" Pretty Print """

	def pretty_print_storage_structure(self):
		containers = self.service.list_containers()
		for container in containers:
			self.pretty_print_container_contents(container.name)

	def pretty_print_container_contents(self, container_name):
		print(container_name)
		blobs = self.service.list_blobs(container_name)
		for blob in blobs:
			print ('  {}'.format(blob.name))

	""" Private """

	def _create_input_container(self):
		self.service.create_container(self.constants.INPUT_CONTAINER_NAME)

	def _create_output_container(self):
		self.service.create_container(self.constants.OUTPUT_CONTAINER_NAME)

	def _create_container(self, container_name):
		self.service.create_container(container_name)

	def _input_container(self):
		return self.constants.INPUT_CONTAINER_NAME

	def _output_container(self):
		return self.constants.OUTPUT_CONTAINER_NAME

	def _get_resource_reference(self, prefix):
		return '{}/{}=={}'.format(prefix, str(uuid.uuid4())[:8], datetime.datetime.now().strftime("%m-%d-%Y %I:%M%p"))

	def _get_blob_reference(self, prefix='blob'):
		return self._get_resource_reference(prefix)

	def _upload_data(self, container_name, path, data):
		if not(self.exists(container_name)):
			self._create_container(container_name)
		blob_name = self._get_blob_reference(path);
		self.service.create_blob_from_text(container_name, blob_name, data)
		self.log(container_name, self.Interacting_Entity, "Up to the load", blob_name)
		return blob_name

	def _download_data(self, container_name, full_blob_name):
		if not(self.exists(container_name)):
			self._create_container(container_name)
		blob = self.service.get_blob_to_text(container_name, full_blob_name)
		content = blob.content
		return content

	def retreive_log_entities(self, container_name, path,  action_filter = None):
		log_entries = LogEntries()
		log_path = path + "/log"
		if self.exists(container_name,log_path):
			log_file = self.service.get_blob_to_text(container_name, log_path)
			raw_logs = log_file.content
			log_entries.deserialize(raw_logs)
		# if(action_filter != None):
		return log_entries

	def log(self, container_name, interacting_entity, action, full_blob_name):
		path = self.get_blobs_parent_directory(full_blob_name)
		log_path = path + '/log'
		log_entries = LogEntries()
		if self.exists(container_name,log_path):
			log_file = self.service.get_blob_to_text(container_name, log_path)
			raw_logs = log_file.content
			log_entries.deserialize(raw_logs)	
		log_entries.append(interacting_entity, action, full_blob_name, UNPROCESSED)
		raw = log_entries.serialize()
		self.service.create_blob_from_text(container_name, log_path, raw)

	def get_blobs_parent_directory(self, full_blob_name):
		return full_blob_name.rsplit('/', 1)[0]

	# def retrieve_logs(self, container, path)
			
	def exists(self, container, full_blob_name = None):
		return self.service.exists(container, full_blob_name)
