from storage_manager import LogoStorageConnector

class IGProccessingDriver:
	def __init__(self):
		self.storage_manager = LogoStorageConnector()

	def start_processing(self):
		print("starting driver...")
		self.brand_names = self.retrieve_supported_brands()
		for brand in self.brand_names:
			blobs = self.retrieve_unproccessed_training_data(brand)
			post_entities_blobs = [blob for blob in blobs if str.endswith(blob.name, "post_entities.txt")]

			for blob in blobs:
				print("  blob name:",blob.name)
				if(blob.content != None):
					print("    blob content:",len(blob.content))

	def retrieve_supported_brands(self):
		return self.storage_manager.get_container_directories("input")

	def retrieve_unproccessed_training_data(self, brand_name):
		return self.storage_manager.download_brand_operational_input_data(brand_name, processing_status_filter="Unprocessed")

	def retrieve_unproccessed_operational_data(self, brand_name):
		return self.storage_manager.download_brand_operational_input_data(brand_name, processing_status_filter="Unprocessed")