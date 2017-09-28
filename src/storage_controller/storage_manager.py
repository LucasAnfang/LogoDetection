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
from instagram_post_entity import InstagramPostEntities
from io import BytesIO
from PIL import Image

class LogoStorageConnector:
	def __init__(self):
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

	""" Public Interfaces """
	""" Upload """
	def upload_brand_training_input_data(self, brand, data, isProcessed):
		container_name = self._input_container()
		path = '{}/{}'.format(brand, self.constants.TRAINING_DIRECTORY_NAME)
		full_blob_name = self._upload_data(container_name, path, data)
		self.log(full_blob_name, isProcessed)
		return  full_blob_name

	def upload_brand_operational_input_data(self, brand, data, isProcessed):
		container_name = self._input_container()
		path = '{}/{}'.format(brand, self.constants.OPERATIONAL_DIRECTORY_NAME)
		full_blob_name = self._upload_data(container_name, path, data)
		self.log(full_blob_name, isProcessed)
		return  full_blob_name

	def upload_brand_training_input_IPE(self, brand, IPE, isProcessed):
		container_name = self._input_container()
		path = '{}/{}'.format(brand, self.constants.TRAINING_DIRECTORY_NAME)
		full_blob_name = self._upload_data(container_name, path, data)
		self.log(full_blob_name, isProcessed)
		return  full_blob_name

	def upload_brand_operational_input_IPE(self, brand, IPE, isProcessed):
		container_name = self._input_container()
		base_path = '{}/{}'.format(brand, self.constants.OPERATIONAL_DIRECTORY_NAME)
		blob_name = self._get_blob_reference(base_path)
		images_dir_path = '{}=={}'.format(blob_name, "images")
		for element in IPE.posts:
			print(element.keys())
			if('picture' in element and 'picture_id' in element):
				path = '{}/{}.png'.format(images_dir_path, element['picture_id'])
				self._upload_and_compress_image(container_name, path, element['picture'])
				element.pop('picture', None)
				element['image_path'] = path
				print("uploading image to path", path)
		print("supplying blob name", blob_name)
		self._upload_data(container_name, base_path, IPE.serialize(), blob_name=blob_name)
		self.log(blob_name, isProcessed)
		return  blob_name

	def upload_brand_operational_output_data(self, brand, data):
		container = self._output_container()
		path = '{}/{}'.format(brand, self.constants.OPERATIONAL_DIRECTORY_NAME)
		return self._upload_data(container, path, data)

	""" Download """
	def download_brand_training_input_data(self, brand, processing_status_filter = None):
		path = '{}/{}'.format(brand, self.constants.TRAINING_DIRECTORY_NAME)
		blobs = []
		container_name = self.constants.INPUT_CONTAINER_NAME
		if(processing_status_filter != None):
			print(path)
			logs = self.retreive_log_entities(container_name, path, processing_status_filter = processing_status_filter)
			for log in logs:
				blobs.append(self._download_data(container_name, log[PATH]))
		else:
			blobs = self.service.list_blobs(container_name=self.constants.INPUT_CONTAINER_NAME, prefix=path)
		return blobs

	def download_brand_operational_input_data(self, brand, processing_status_filter = None):
		path = '{}/{}'.format(brand, self.constants.OPERATIONAL_DIRECTORY_NAME)
		blobs = []
		container_name = self.constants.INPUT_CONTAINER_NAME
		if(processing_status_filter != None):
			logs = self.retreive_log_entities(container_name, path, processing_status_filter = processing_status_filter)
			for log in logs:
				blobs.append(self._download_data(container_name, log[PATH]))
		else:
			blobs = self.service.list_blobs(container_name=self.constants.INPUT_CONTAINER_NAME, prefix=path)
		return blobs

	def download_brand_operational_output_data(self, brand):
		path = '{}/{}'.format(brand, self.constants.OPERATIONAL_DIRECTORY_NAME)
		blobs = self.service.list_blobs(container_name=self.constants.OUTPUT_CONTAINER_NAME, prefix=path)
		return blobs

	def get_container_directories(self, container_name):
		bloblistingresult = self.service.list_blobs(container_name=container_name, delimiter='/') 
		return [blob.name.rsplit('/', 1)[0] for blob in bloblistingresult]

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
		return '{}/{}=={}.txt'.format(prefix, str(uuid.uuid4())[:8], datetime.datetime.now().strftime("%m-%d-%Y %I:%M%p"))

	def _get_blob_reference(self, prefix='blob'):
		return self._get_resource_reference(prefix)

	def _upload_data(self, container_name, path, data, blob_name = None):
		if not(self.exists(container_name)):
			self._create_container(container_name)
		if not (blob_name == None):
			blob_name = self._get_blob_reference(path);
			print("Getting new blob name", blob_name)
		self.service.create_blob_from_text(container_name, blob_name, data)
		return blob_name

	def _upload_and_compress_image(self, container_name, full_blob_name, data):
		if not(self.exists(container_name)):
			self._create_container(container_name)

		with BytesIO() as output:
			data.save(output, 'PNG')
			bytes = output.getvalue()
		self.service.create_blob_from_bytes(container_name, full_blob_name, bytes)
		return full_blob_name

	def _download_data(self, container_name, full_blob_name):
		if not(self.exists(container_name)):
			self._create_container(container_name)
		blob = self.service.get_blob_to_text(container_name, full_blob_name)
		content = blob.content
		return blob

	def retreive_log_entities(self, container_name, path, processing_status_filter = None):
		log_entries = LogEntries()
		log_path = path + "/log.txt"
		if self.exists(container_name,log_path):
			log_file = self.service.get_blob_to_text(container_name, log_path)
			raw_logs = log_file.content
			log_entries.deserialize(raw_logs)
		if(processing_status_filter != None):
			log_entries = log_entries.GetLogs(processing_status_filter=processing_status_filter)
		return log_entries

	def log(self, full_blob_name, isProcessed):
		container_name = self._input_container()
		path = self.get_blobs_parent_directory(full_blob_name)
		log_path = path + '/log.txt'
		log_entries = LogEntries()
		if self.exists(container_name,log_path):
			log_file = self.service.get_blob_to_text(container_name, log_path)
			raw_logs = log_file.content
			log_entries.deserialize(raw_logs)	
		log_entries.update(full_blob_name, isProcessed=isProcessed)
		raw = log_entries.serialize()
		self.service.create_blob_from_text(container_name, log_path, raw)

	def update_log_entries(self, full_blob_names, isProcessed):
		directories = {}
		container_name = self._input_container()
		for full_blob_name in full_blob_names:
			path = self.get_blobs_parent_directory(full_blob_name)
			log_path = path + '/log.txt'
			if log_path in directories:
				directories[log_path].append(full_blob_name)
			else:
				directories[log_path] = []
				directories[log_path].append(full_blob_name)
		for key, value in directories.iteritems():
			log_entries = LogEntries()
			if self.exists(container_name, key):
				log_file = self.service.get_blob_to_text(container_name, key)
				raw_logs = log_file.content
				log_entries.deserialize(raw_logs)
			for full_blob_name in value:
				log_entries.update(full_blob_name, isProcessed=isProcessed)
			raw = log_entries.serialize()
			self.service.create_blob_from_text(container_name, log_path, raw)
		
	def get_blobs_parent_directory(self, full_blob_name):
		return full_blob_name.rsplit('/', 1)[0]
			
	def exists(self, container, full_blob_name = None):
		return self.service.exists(container, full_blob_name)
