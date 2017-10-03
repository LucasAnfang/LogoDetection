from storage_manager import LogoStorageConnector
from instagram_post_entities import InstagramPostEntities

class IGProccessingDriver:
	def __init__(self):
		self.storage_manager = LogoStorageConnector()

	def start_processing(self):
		print("starting driver...")
		self.brand_names = self.retrieve_supported_brands()
		for brand in self.brand_names:
			post_entities_blobs = self.retrieve_unproccessed_operational_post_entities(brand)
			for blob in blobs:
				print blob.name
				print blob.content

	def retrieve_supported_brands(self):
		return self.storage_manager.get_container_directories("input")

	def extract_post_entities_data(self, post_entities_blobs, isTraining = False, isOperational = False):
		if(isTraining == isOperational):
			raise ValueError('IG post entities has to be either training or operational (not both)')
		self.brand_to_post_entities_list = {}
		for post_entities in post_entities_blobs:
			brand_name = post_entities.name.split('/')[0]
			if brand_name in self.brand_to_post_entities_list
				ipe = InstagramPostEntities(isTraining = isTraining, isClassification = isOperational, serialized_obj = None)
				self.brand_to_post_entities_list[brand_name].append(ipe)

	def retrieve_unproccessed_training_post_entities(self, brand_name):
		return self.storage_manager.download_brand_training_input_post_entities(brand_name, processing_status_filter="Unprocessed")

	def retrieve_unproccessed_operational_post_entities(self, brand_name):
		return self.storage_manager.download_brand_operational_input_post_entities(brand_name, processing_status_filter="Unprocessed")

	def retrieve_unproccessed_training_data(self, brand_name):
		return self.storage_manager.download_brand_operational_input_data(brand_name, processing_status_filter="Unprocessed")

	def retrieve_unproccessed_operational_data(self, brand_name):
		return self.storage_manager.download_brand_operational_input_data(brand_name, processing_status_filter="Unprocessed")