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
from log_entries_base import *
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
    def get_containers(self):
        containers = self.service.list_containers()
        return containers

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
	def parallel_chunky_upload(self, container_name, full_blob_name, data, chunks = 5):
		debug = False
		threads = []
		block_ids = []
		chunk_size = len(data) / chunks
		chunks = [data[i:i + chunk_size] for i in xrange(0, len(data), chunk_size)]
		for chunk in chunks:
			uid = self.generate_uid()
			block_ids.append(BlobBlock(id=uid))
			t = threading.Thread(target=self._upload_block, args=(container_name,full_blob_name,chunk,uid,))
			threads.append(t)
			t.start()
		[t.join() for t in threads]
		self.service.put_block_list(container_name, full_blob_name, block_ids)
        return full_blob_name

	def _upload_block(self, container_name, full_blob_name, chunk, uid):
		self.service.put_block(container_name, full_blob_name, chunk, uid)

	def upload_text(self, container_name, full_blob_name, data):
		if not(self.exists(container_name)):
			self._create_container(container_name)
		self.service.create_blob_from_text(container_name, full_blob_name, data)
		return full_blob_name

	def upload_image(self, container_name, path, data):
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
	def retreive_log_entities(self, container_name, path, log_entries, filter_dictionary = None):
		log_path = '{}/log.txt'.format(path)
		if self.exists(container_name,log_path):
			log_file = self.service.get_blob_to_text(container_name, log_path)
			raw_logs = log_file.content
			log_entries.deserialize(raw_logs)
		if(filter_dictionary != None):
			log_entries = log_entries.GetLogs(filter=filter_dictionary)

	def update_log(self, container_name, log_entries, entry):
		path = self.get_parent_directory(log_entry['prefix'])
		log_path = '{}/log.txt'.format(path)
		if self.exists(container_name,log_path):
			log_file = self.service.get_blob_to_text(container_name, log_path)
			raw_logs = log_file.content
			log_entries.deserialize(raw_logs)
		log_entries.update(entry)
		raw = log_entries.serialize()
		self.service.create_blob_from_text(container_name, log_path, raw)
        return log_entries

	def update_logs(self, container_name, log_entries, entries):
        log_paths = {'{}/log.txt'.format(self.get_parent_directory(log_entry['prefix'])) for log_entry in entries}
        if len(log_paths) > 1:
            raise ValueError('Logs being updated must be of the same log file')
        log_path = log_paths[0]
		if not self.exists(container_name,log_path):
            raise ValueError('Log file {} under container {} does not exist'.format(log_path, container_name))
		log_file = self.service.get_blob_to_text(container_name, log_path)
        raw_logs = log_file.content
        log_entries.deserialize(raw_logs)
		for entry in entries:
			log_entries.update(entry)
		raw = log_entries.serialize()
		self.service.create_blob_from_text(container_name, log_path, raw)
        return log_entries


	def update_log_entries(self, container_name, mlog_entries, entity_names, patch_dictionary):
		directories = {}
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
			log_entries = LogEntriesBase()
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

    def _organize_entities_by(entity_names)
    """ Pretty Print """
	def pretty_print_storage_structure(self):
		containers = self.service.list_containers()
		for container in containers:
			self.pretty_print_container_contents(container.name)
