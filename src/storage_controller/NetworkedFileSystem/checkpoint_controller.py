import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../..'))
from src.storage_controller.Entities.log_entries_base import LogEntriesBase
from src.storage_controller.Entities.input_log_entries import InputLogEntries
from src.storage_controller.Entities.instagram_post_entity import InstagramPostEntities
from nfs_controller_config import NFS_Controller_Config
from nfs_controller import NFS_Controller
import uuid
import datetime

class CheckpointController:
	def __init__(self, config):
		try:
			import nfs_constants as constants
			self.constants = constants
		except:
			raise ValueError('Please specify networked file system contants in nfs_constants.py.')
		self.nfs_controller = NFS_Controller(config)
		self._create_checkpoint_container()

	""" Input Utility """
	def _create_checkpoint_container(self):
		self.nfs_controller.create_container(self._checkpoint_container())

	def _checkpoint_container(self):
		return self.constants.CHECKPOINTS_CONTAINER_NAME

	def get_container_directories(self):
		return self.nfs_controller.get_container_directories(self._checkpoint_container())

	""" Upload """
	def upload_checkpoints(self, origin_directory):
		self.nfs_controller.batched_parallel_directory_upload(self._checkpoint_container(), "", origin_directory, ext_filter_list = None)

	""" Download """
	def download_checkpoints(self, destination_directory = None):
		print "download checkpoints " + destination_directory
		self.nfs_controller.download_full_container(self._checkpoint_container(), destination_directory = destination_directory)

	def parallel_download(self, full_blob_names):
		return self.nfs_controller.parallel_download(self._input_container(), full_blob_names)

	def download_data(self, full_blob_name):
		container = self._input_container()
		return self.nfs_controller.download_data(container, full_blob_name)
