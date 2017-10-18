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
	def retreive_log_entities(self, container_name, path, mlog_entries, filter_dictionary = None):
		log_path = '{}/log.txt'.format(path)
		if self.exists(container_name,log_path):
			log_file = self.service.get_blob_to_text(container_name, log_path)
			raw_logs = log_file.content
			mlog_entries.deserialize(raw_logs)
		if(filter_dictionary != None):
			mlog_entries = mlog_entries.GetLogs(filter=filter_dictionary)

	def update_log(self, container_name, mlog_entries, entry):
		path = self.get_parent_directory(entry['path'])
		log_path = '{}/log.txt'.format(path)
		if self.exists(container_name,log_path):
			log_file = self.service.get_blob_to_text(container_name, log_path)
			raw_logs = log_file.content
			mlog_entries.deserialize(raw_logs)
		mlog_entries.update(entry)
		raw = mlog_entries.serialize()
		self.service.create_blob_from_text(container_name, log_path, raw)

	def update_logs(self, container_name, mlog_entries, entries):
        log_paths = {'{}/log.txt'.format(self.get_parent_directory(log_entry['path'])) for log_entry in entries}
        if len(log_paths) > 1:
            raise ValueError('Logs being updated must be of the same log file')
        log_path = log_paths[0]
		if not self.exists(container_name,log_path):
            raise ValueError('Log file {} under container {} does not exist'.format(log_path, container_name))
		log_file = self.service.get_blob_to_text(container_name, log_path)
        raw_logs = log_file.content
        mlog_entries.deserialize(raw_logs)
		for entry in entries:
			mlog_entries.update(entry)
		raw = mlog_entries.serialize()
		self.service.create_blob_from_text(container_name, log_path, raw)

    """ Avoid Using this: It is not efficient and you should always update a log directly after resource use """
	def update_multiple_log_files(self, container_name, mlog_entries, entries):
        log_paths = {'{}/log.txt'.format(self.get_parent_directory(log_entry['path'])) for log_entry in entries}
		for log_path in log_paths:
            entries = [log_entry for log_entry in entries if '{}/log.txt'.format(self.get_parent_directory(log_entry['path'])) == log_path]
            self.update_log_file(container_name, mlog_entries, entries)
            mlog_entries.ResetLogs()
