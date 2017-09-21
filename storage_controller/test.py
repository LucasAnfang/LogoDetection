from storage_manager import LogoStorageConnector
lsc = LogoStorageConnector()

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

upload_demo = False
if(upload_demo == True):
	brand_names = ["Puma", "Lego", "Nike", "Adidas", "Patagonia"]
	print("Demo for upload to various directories for", brand_names)
	for brand_name in brand_names:
		print("\nUploading ", brand_name, " Training Data [UNPROCESSED]")
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_1", isProcessed = False))
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_2", isProcessed = False))
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_3", isProcessed = False))

		print("\nUploading ", brand_name, " Operational Data [UNPROCESSED]")
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_1", isProcessed = False))
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_2", isProcessed = False))
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_3", isProcessed = False))

		print("\nUploading ", brand_name, " Training Data [PROCESSED]")
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_1", isProcessed = True))
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_2", isProcessed = True))
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_3", isProcessed = True))

		print("\nUploading ", brand_name, " Operational Data [PROCESSED]")
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_1", isProcessed = True))
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_2", isProcessed = True))
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_3", isProcessed = True))

print("These are the current brands being supprted or sleighted to be processed")
vds = lsc.get_container_directories("input")
for entity in vds:
	print('[',entity,']')


log_demo = True
if(log_demo == True):
	brand_names = ["Puma", "Lego", "Nike", "Adidas", "Patagonia"]
	print("Demo for analyzing logs for multiple brands and their existing directories", brand_names)
	for brand_name in brand_names:
		path = brand_name + "/training"
		print("====================",path,"====================")
		unprocessed_logs = lsc.retreive_log_entities("input", "Patagonia/training", "Unprocessed")
		for entity in unprocessed_logs:
			print(" path [", entity['Path'],"] Processing Status: [", entity['Processing_Status'], "]")
		processed_logs = lsc.retreive_log_entities("input", "Patagonia/training", "Processed")
		for entity in processed_logs:
			print(" path [", entity['Path'],"] Processing Status: [", entity['Processing_Status'], "]")
		print("=====================================================")

		path = brand_name + "/operational"
		print("====================",path,"====================")
		unprocessed_logs = lsc.retreive_log_entities("input", "Patagonia/operational", "Unprocessed")
		for entity in unprocessed_logs:
			print(" path [", entity['Path'],"] Processing Status: [", entity['Processing_Status'], "]")
		processed_logs = lsc.retreive_log_entities("input", "Patagonia/operational", "Processed")
		for entity in processed_logs:
			print(" path [", entity['Path'],"] Processing Status: [", entity['Processing_Status'], "]")
		print("=====================================================")

blobs = lsc.download_brand_training_input_data("Patagonia", processing_status_filter="Unprocessed")
for blob in blobs:
	print(blob.name)
	print(blob.content)