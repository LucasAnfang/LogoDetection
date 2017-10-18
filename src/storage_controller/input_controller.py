from . import log_entries
from .instagram_post_entity import InstagramPostEntities
from .nfs_controller import NFS_Controller

class InputConnector:
	def __init__(self):
		try:
			import nfs_config as config
			self.config = config
		except:
			raise ValueError('Please specify configuration settings in config.py.')
		try:
			import constants as constants
			self.constants = constants
		except:
			raise ValueError('Please specify networked file system contants in nfs_constants.py.')
        self.nfs_controller = NFS_Controller(config)
		self._create_input_container()

	""" Input Utility """
    	def _create_path_to_bucket(self, brand_name, level):
    		return '{}/{}/{}=={}'.format(brand_name, level, str(uuid.uuid4())[:8], datetime.datetime.now().strftime("%m-%d-%Y %I:%M%p"))

    	def _get_bucket_image_directory(self, prefix):
    		return '{}/[IMAGES]'.format(prefix)

    	def _get_bucket_post_entities_file(self, prefix):
    		return '{}/post_entities.txt'.format(prefix)

    	def _input_container(self):
    		return self.constants.INPUT_CONTAINER_NAME

    	def get_container_directories(self, container_name):
    		return self.nfs_controller.get_container_directories(container_name)
	""" Upload: input """

	def upload_brand_training_input_IPE(self, brand, IPE, isProcessed):
		return self.upload_IPE_to_bucket(self._input_container(), brand, self.constants.TRAINING_DIRECTORY_NAME, IPE, isProcessed, log = True)

	def upload_brand_operational_input_IPE(self, brand, IPE, isProcessed):
		return self.upload_IPE_to_bucket(self._input_container(), brand, self.constants.OPERATIONAL_DIRECTORY_NAME, IPE, isProcessed, log = True)

	def upload_IPE_to_bucket(self, container_name, brand, directory, IPE, isProcessed, log = True):
		bucket_path = self._create_path_to_bucket(brand, directory)
		bucket_post_entities_full_path = self._get_bucket_post_entities_file(bucket_path)
		bucket_images_base_path = self._get_bucket_image_directory(bucket_path)
		for element in IPE.posts:
			print(element.keys())
			if('picture' in element and 'picture_id' in element):
				path = '{}/{}'.format(bucket_images_base_path, element['picture_id'])
				image_path = self.nfs_controller.upload_image(container_name, self._input_container(), path, element['picture'])
				element.pop('picture', None)
				element['image_path'] = image_path
		self.nfs_controller.upload_text(container_name, bucket_post_entities_full_path, IPE.serialize())
		if(log == True):
			\self.log(bucket_path, isProcessed)
		return  bucket_path

	""" Download """
	def download_brand_training_input_post_entities(self, brand, processing_status_filter = None):
		prefix = '{}/{}'.format(brand, self.constants.TRAINING_DIRECTORY_NAME)
		return self.download_brand_post_entities(self.constants.INPUT_CONTAINER_NAME, brand, prefix, processing_status_filter = processing_status_filter)

	def download_brand_operational_input_post_entities(self, brand, processing_status_filter = None):
		prefix = '{}/{}'.format(brand, self.constants.OPERATIONAL_DIRECTORY_NAME)
		return self.download_brand_post_entities(self.constants.INPUT_CONTAINER_NAME, brand, prefix, processing_status_filter = processing_status_filter)

	def download_brand_post_entities(self, brand, prefix, processing_status_filter = None):
		blobs = []
        container_name = self.constants.INPUT_CONTAINER_NAME
		\logs = self.retreive_log_entities(container_name, prefix)
		if(processing_status_filter != None):
			\unproccessed_entries = logs.GetLogs(processing_status_filter = processing_status_filter)
			for log in unproccessed_entries:
				blobs.append(self.nfs_controller.download_data(container_name, '{}/{}'.format(log[PREFIX], 'post_entities.txt')))
		else:
			for log in logs:
				blobs.append(self.nfs_controller.download_data(container_name, '{}/{}'.format(log[PREFIX], 'post_entities.txt')))
		return blobs

	def parallel_download(self, full_blob_names):
		return self.nfs_controller.parallel_download(self.constants.INPUT_CONTAINER_NAME, full_blob_names)

	def download_data(self, container_name, full_blob_name):
        container = self.constants.INPUT_CONTAINER_NAME
		return self.nfs_controller.download_data(container, full_blob_name)

	def retreive_log_entities(self, container_name, path, processing_status_filter = None):
        logs = LogEntriesBase()
	def log(self, prefix, isProcessed):

	def update_log_entries(self, bucket_names, isProcessed):
