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

class NFS_Controller:
	def __init__(self, config):
		self.config = config
		self.account = CloudStorageAccount(account_name=config.STORAGE_ACCOUNT_NAME, account_key=config.STORAGE_ACCOUNT_KEY)
		self.service = self.account.create_block_blob_service()

    """ utility functions """
	def get_container_directories(self, container_name):
		bloblistingresult = self.service.list_blobs(container_name=container_name, delimiter='/')
		return [blob.name.rsplit('/', 1)[0] for blob in bloblistingresult]

	def create_container(self, container_name):
		self.service.create_container(container_name)

    def get_parent_directory(self, path):
    	return path.rsplit('/', 1)[0]

	def exists(self, container, full_blob_name = None):
		return self.service.exists(container, full_blob_name)

	def generate_uid(self):
		r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
		return r_uuid.replace('=', '')

	""" Upload: """
	def parallel_chunky_upload(self, container_name, full_blob_name, data):
		debug = False
		threads = []
		block_ids = []

		chunk_size = len(data) / 5
		if (debug):
			print "chunking data into even sections of length: ", chunk_size
		chunks = [data[i:i + chunk_size] for i in xrange(0, len(data), chunk_size)]

		for chunk in chunks:
			uid = self.generate_uid()
			block_ids.append(BlobBlock(id=uid))
			if (debug):
				print "spawning thread with uid: ", uid
			t = threading.Thread(target=self._upload_block, args=(container_name,full_blob_name,chunk,uid,))
			threads.append(t)
			t.start()
		if (debug):
			print "all threads started..."
		[t.join() for t in threads]
		if (debug):
			print "all threads have completed execution"

		if (debug):
			block_list = self.service.get_block_list(container_name, full_blob_name, block_list_type=BlockListType.All)
			uncommitted = len(block_list.uncommitted_blocks)
			committed = len(block_list.committed_blocks)
		 	print "uncommitted: ", uncommitted, " committed: ", committed

		if (debug):
			print "committing blocks"

		self.service.put_block_list(container_name, full_blob_name, block_ids)

		if (debug):
			block_list = self.service.get_block_list(container_name, full_blob_name, block_list_type=BlockListType.All)
			uncommitted = len(block_list.uncommitted_blocks)
			committed = len(block_list.committed_blocks)
			print "uncommitted: ", uncommitted, " committed: ", committed

	def _upload_block(self, container_name, full_blob_name, chunk, uid):
		self.service.put_block(container_name, full_blob_name, chunk, uid)

	def _upload_text(self, container_name, full_blob_name, data):
		if not(self.exists(container_name)):
			self._create_container(container_name)
		self.service.create_blob_from_text(container_name, full_blob_name, data)
		return full_blob_name

	def _upload_image(self, container_name, path, data):
		if not(self.exists(container_name)):
			self._create_container(container_name)
		full_blob_name = '{}{}'.format(path, '.jpeg')
		with BytesIO() as output:
			data.save(output, 'jpeg')
			image_bytes = output.getvalue()
		self._parallel_upload(container_name, full_blob_name, image_bytes)
		return full_blob_name

	""" Download """
	def parallel_image_download(self, container_name, full_blob_names):
		if(full_blob_names == None):
			return None
		threads = []
		results = []
		for full_blob_name in full_blob_names:
			result = {'blob': None}
			t = threading.Thread(target=self._download_blob_helper, args=(container_name,full_blob_name, result))
			results.append(result)
			threads.append(t)
			t.start()
		[t.join() for t in threads]
		blobs = [result['blob'] for result in results if result['blob'] != None]
		return blobs

	def _download_blob_helper(self, container_name, full_blob_name, result):
		if(self.exists(container_name, full_blob_name)):
			result['blob'] = self._download_data(container_name, full_blob_name)
		else:
			return None

	def download_data(self, container_name, full_blob_name):
		if not(self.exists(container_name)):
			self._create_container(container_name)
            return None
        blob = self.service.get_blob_to_bytes(container_name, full_blob_name)
        return blob
    
    """ Logging """
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

	def update_log_entries(self, bucket_names, isProcessed):
		directories = {}
		container_name = self._input_container()
		for bucket_name in bucket_names:
			print(bucket_name)
			path = self.get_parent_directory(bucket_name)
			print(path)
			log_path = path + '/log.txt'
			print(directories.keys())
			if log_path in directories:
				directories[log_path].append(bucket_name)
			else:
				print("adding new log path: ", log_path)
				directories[log_path] = []
				directories[log_path].append(bucket_name)
		for key, value in directories.iteritems():
			log_entries = LogEntries()
			if self.exists(container_name, key):
				log_file = self.service.get_blob_to_text(container_name, key)
				raw_logs = log_file.content
				print(key)
				print(raw_logs)
				log_entries.deserialize(raw_logs)
			for bucket_name in value:
				print("updating for bucket_name:", bucket_name, "for file: ", key)
				log_entries.update(bucket_name, isProcessed=isProcessed)
				print (log_entries.serialize())
			raw = log_entries.serialize()
			self.service.create_blob_from_text(container_name, key, raw)

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
