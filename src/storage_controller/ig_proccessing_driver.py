from storage_manager import LogoStorageConnector
from instagram_post_entity import InstagramPostEntities

class IGProccessingDriver:
	def __init__(self):
		self.storage_manager = LogoStorageConnector()

	def start_processing(self):
		print("starting driver...")
		self.brand_names = self.retrieve_supported_brands()
		for brand in self.brand_names:
			post_entities_blobs = self.retrieve_unproccessed_training_post_entities(brand)
			if(len(post_entities_blobs) != 0):
				training_post_entities_list = self.extract_post_entities_data(post_entities_blobs, isTraining = True)
				self.process_training_post_entries(training_post_entities_list, isTraining = True)
			else:
				print("No training data to be processed")

			post_entities_blobs = self.retrieve_unproccessed_operational_post_entities(brand)
			if(len(post_entities_blobs) != 0):
				operational_post_entities_list = self.extract_post_entities_data(post_entities_blobs, isOperational = True)
				self.process_operational_post_entries(operational_post_entities_list, isOperational = True)
			else:
				print("No operational data to be processed")

	def process_operational_post_entries(self, post_entities_list, isTraining = False, isOperational = False):
		for post_entities in post_entities_list:
			image_paths = [post_entity['image_path'] for post_entity in post_entities.posts]
			r2d2 = R2D2(self.storage_manager)
			r2d2.set_image_paths(image_paths)
			for post_entity in post_entities.posts:
				image_bytes = r2d2.get_image_with_path(post_entity['image_path'])

	def process_training_post_entries(self, post_entities_list, isTraining = False, isOperational = False):
		for post_entities in post_entities_list:

			no_logo_post_entities = [post_entity for post_entity in post_entities.posts if post_entity['has_logo'] = False]
			logo_post_entities = [post_entity for post_entity in post_entities.posts if post_entity['has_logo'] = True]

			no_logo_image_paths = [post_entity['image_path'] for post_entity in no_logo_post_entities.posts]
			logo_image_paths = [post_entity['image_path'] for post_entity in logo_post_entities.posts]

			no_logo_r2d2 = R2D2(self.storage_manager)
			logo_r2d2 = R2D2(self.storage_manager)

			no_logo_r2d2.set_image_paths(no_logo_image_paths)
			logo_r2d2.set_image_paths(logo_image_paths)

			for post_entity in post_entities.posts:
				image_bytes = r2d2.get_image_with_path(post_entity['image_path'])


	def retrieve_supported_brands(self):
		return self.storage_manager.get_container_directories("input")

	def extract_post_entities_data(self, post_entities_blobs, isTraining = False, isOperational = False):
		if(isTraining == isOperational):
			raise ValueError('IG post entities has to be either training or operational (not both)')
		post_entities_list = []
		for post_entities in post_entities_blobs:
			brand_name = post_entities.name.split('/')[0]
			ipe = InstagramPostEntities(isTraining = isTraining, isClassification = isOperational)
			ipe.deserialize(post_entities.content)
			print("extracting ipe data for brand", brand_name, "from resource", post_entities.name)
			post_entities_list.append(ipe)
		return post_entities_list

	def retrieve_unproccessed_training_post_entities(self, brand_name):
		return self.storage_manager.download_brand_training_input_post_entities(brand_name, processing_status_filter="Unprocessed")

	def retrieve_unproccessed_operational_post_entities(self, brand_name):
		return self.storage_manager.download_brand_operational_input_post_entities(brand_name, processing_status_filter="Unprocessed")

class R2D2:
	def __init__(self, storage_manager):
		self.storage_manager = storage_manager

	def reset(self):
		self.current_index = 0
		self.cache = []

	def set_image_paths(self, image_paths, batch_size = 10):
		self.image_paths = image_paths
		self.batch_size = batch_size
		self.reset()
		self.batch_download()

	def is_cache_empty(self):
		return (len(self.cache) == 0)

	def get_image_with_path(self, full_blob_name):
		if(self.is_cache_empty() == True):
			self.batch_download()
		return self.get_blob_from_cache(full_blob_name)
		# print "downloading image from path: " + full_blob_name
		# return self.download_data(full_blob_name)
	
	def get_blob_from_cache(self, full_blob_name):
		blob = None
		for index in range(len(self.cache)):
			if(self.cache[index].name == full_blob_name):
				print "blob with path: " + full_blob_name + " found in cache"
				blob = self.cache[index].name
				self.cache.pop(index)
				break
		if(blob == None):
			blob = self.download_data(full_blob_name)
			print "blob with path: " + full_blob_name + " NOT found in cache"
		return blob

	def download_data(self, full_blob_name):
		return self.storage_manager.download_input_data(full_blob_name)

	def batch_download(self):
		if(self.is_cache_empty() == False):
			return
		indices = [(self.current_index + i) for i in range(self.batch_size)]
		paths = [self.image_paths[i] for i in indices if (i < len(self.image_paths))]
		print "downloading next batch to cache..."
		self.current_index += len(paths)
		if(len(paths) != 0):
			self.cache.extend(self.storage_manager.parallel_input_image_download(paths))


		


























