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
from io import BytesIO
import zlib
import threading
import base64
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

	def upload_brand_training_input_IPE(self, brand, IPE, isProcessed):
		return self.upload_IPE_to_bucket(self._input_container(), brand, self.constants.TRAINING_DIRECTORY_NAME, IPE, isProcessed, log = True)

	def upload_brand_operational_input_IPE(self, brand, IPE, isProcessed):
		return self.upload_IPE_to_bucket(self._input_container(), brand, self.constants.OPERATIONAL_DIRECTORY_NAME, IPE, isProcessed, log = True)

	def upload_IPE_to_bucket(self, container_name, brand, directory, IPE, isProcessed, log = False):
		bucket_path = self._create_path_to_bucket(brand, directory)
		bucket_post_entities_full_path = self._get_bucket_post_entities_file(bucket_path)
		bucket_images_base_path = self._get_bucket_image_directory(bucket_path)
		for element in IPE.posts:
			print(element.keys())
			if('picture' in element and 'picture_id' in element):
				path = '{}/{}'.format(bucket_images_base_path, element['picture_id'])
				image_path = self._upload_and_compress_image(container_name, path, element['picture'])
				element.pop('picture', None)
				element['image_path'] = image_path
		self._upload_text(container_name, bucket_post_entities_full_path, IPE.serialize())
		if(log == True):
			self.log(bucket_path, isProcessed)
		return  bucket_path

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

	def _create_path_to_bucket(self, brand_name, level):
		return '{}/{}/{}=={}'.format(brand_name, level, str(uuid.uuid4())[:8], datetime.datetime.now().strftime("%m-%d-%Y %I:%M%p"))

	def _get_bucket_image_directory(self, prefix):
		return '{}/[IMAGES]'.format(prefix)

	def _get_bucket_post_entities_file(self, prefix):
		return '{}/post_entities.txt'.format(prefix)

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

	def get_parent_directory(self, entity):
		return entity.rsplit('/', 1)[0]
			
	def exists(self, container, full_blob_name = None):
		return self.service.exists(container, full_blob_name)

	def _upload_text(self, container_name, full_blob_name, data):
		if not(self.exists(container_name)):
			self._create_container(container_name)
		print("uploading text to path", full_blob_name)
		self.service.create_blob_from_text(container_name, full_blob_name, data)
		return full_blob_name

	def _upload_and_compress_image(self, container_name, path, data):
		if not(self.exists(container_name)):
			self._create_container(container_name)
		full_blob_name = '{}{}'.format(path, '.png')

		with BytesIO() as output:
			data.save(output, 'PNG')
			bytes = output.getvalue()

		print("uploading image to path", path)
		self._parallel_upload(container_name, full_blob_name, bytes)
		return full_blob_name

	def _parallel_upload(self, container_name, full_blob_name, data):
		debug = True
		threads = []
		thread_count = 10
		block_ids = []

		current_index = 0
		end_index = len(data) - 1

		offset = end_index / thread_count

		n = len(data) / 5
		if (debug):
			print("chunking data into even sections of length: ", n)
		chunks = [data[i:i + n] for i in xrange(0, len(data), n)]

		for chunk in chunks:
			uid = self.generate_uid()#[str(uuid.uuid4())[:4]]
			block_ids.append(BlobBlock(id=uid))
			if (debug):
				print("spawning thread with uid: ", uid)
			t = threading.Thread(target=self._upload_block, args=(container_name,full_blob_name,chunk,uid,))
			threads.append(t)
		if (debug):	
			print("starting all the threads...")
		[t.start() for t in threads]
		if (debug):	
			print("all threads started...")
		[t.join() for t in threads]
		if (debug):	
			print("all threads have completed execution")

		block_list = self.service.get_block_list(container_name, full_blob_name, block_list_type=BlockListType.All)
		uncommitted = len(block_list.uncommitted_blocks)
		committed = len(block_list.committed_blocks)
		if (debug):	
			print("uncommitted: ", uncommitted, " committed: ", committed)

		if (debug):	
			print("committing blocks")
		self.service.put_block_list(container_name, full_blob_name, block_ids)

		block_list = self.service.get_block_list(container_name, full_blob_name, block_list_type=BlockListType.All)
		uncommitted = len(block_list.uncommitted_blocks)
		committed = len(block_list.committed_blocks)
		if (debug):	
			print("uncommitted: ", uncommitted, " committed: ", committed)

	def _upload_block(self, container_name, full_blob_name, chunk, uid):
		self.service.put_block(container_name, full_blob_name, chunk, uid)

	def generate_uid(self):
		r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
		return r_uuid.replace('=', '')

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

	def log(self, prefix, isProcessed):
		container_name = self._input_container()
		path = self.get_parent_directory(prefix)
		log_path = path + '/log.txt'
		log_entries = LogEntries()
		if self.exists(container_name,log_path):
			log_file = self.service.get_blob_to_text(container_name, log_path)
			raw_logs = log_file.content
			log_entries.deserialize(raw_logs)	
		log_entries.update(prefix, isProcessed=isProcessed)
		raw = log_entries.serialize()
		self.service.create_blob_from_text(container_name, log_path, raw)

	def update_log_entries(self, bucket_name, isProcessed):
		directories = {}
		container_name = self._input_container()
		for full_blob_name in full_blob_names:
			path = self.get_blobs_parent_directory(bucket_name)
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
