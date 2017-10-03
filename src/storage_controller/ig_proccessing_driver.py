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
			training_post_entities_list = self.extract_post_entities_data(post_entities_blobs, isTraining = True)
			if(training_post_entities_list != None):
				self.process_post_entries(training_post_entities_list, isTraining = True)
			else:
				print("No training data to be processed")

			post_entities_blobs = self.retrieve_unproccessed_operational_post_entities(brand)
			operational_post_entities_list = self.extract_post_entities_data(post_entities_blobs, isOperational = True)
			if(operational_post_entities_list != None):
				self.process_post_entries(operational_post_entities_list, isOperational = True)
			else:
				print("No operational data to be processed")

	def process_post_entries(self, post_entities_list, isTraining = False, isOperational = False):
		

	def retrieve_supported_brands(self):
		return self.storage_manager.get_container_directories("input")

	def extract_post_entities_data_nonoland(self, post_entities_blobs, isTraining = False, isOperational = False):
		if(isTraining == isOperational):
			raise ValueError('IG post entities has to be either training or operational (not both)')
		self.brand_to_post_entities_list = {}
		for post_entities in post_entities_blobs:
			brand_name = post_entities.name.split('/')[0]
			if brand_name in self.brand_to_post_entities_list:
				ipe = InstagramPostEntities(isTraining = isTraining, isClassification = isOperational)
				ipe.deserialize(post_entities.content)
				print("extracting ipe data for brand", brand_name, "from resource", post_entities.name)
				self.brand_to_post_entities_list[brand_name].append(ipe)

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

	def retrieve_unproccessed_training_data(self, brand_name):
		return self.storage_manager.download_brand_operational_input_data(brand_name, processing_status_filter="Unprocessed")

	def retrieve_unproccessed_operational_data(self, brand_name):
		return self.storage_manager.download_brand_operational_input_data(brand_name, processing_status_filter="Unprocessed")