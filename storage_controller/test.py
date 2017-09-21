from storage_manager import LogoStorageConnector
lsc = LogoStorageConnector("IG_SCRAPER")

#lsc.upload_brand_training_input_data("Patagonia", "IMAGE_SET_1")
# lsc.upload_brand_operational_input_data("Patagonia", "IMAGE_SET_1")
 # lsc.upload_brand_operational_output_data("Patagonia", "IMAGE_SET_1")
# lsc.download_brand_training_input_data("Patagonia")

# logs = lsc.retreive_log_entities("input", "Patagonia/operational", "Unprocessed")
# for entity in logs:
# 	print(" path ", entity['Path']," Processing Status ", entity['Processing_Status'])

# vds = lsc.get_container_directories("input")
# for entity in vds:
# 	print('[',entity,']')

# blobs = lsc.download_brand_training_input_data("input", "Patagonia")

blob_name = lsc.upload_brand_training_input_data("Patagonia", "IMAGE_SET_1", isProcessed = False)
lsc.download_brand_training_input_data("Patagonia", processing_status_filter="Unprocessed")