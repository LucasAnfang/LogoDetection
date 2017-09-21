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
		print("Uploading ", brand_name, " Training Data")
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_1", isProcessed = False))
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_2", isProcessed = False))
		print(lsc.upload_brand_training_input_data(brand_name, "IMAGE_SET_3", isProcessed = False))

		print("Uploading ", brand_name, " Operational Data")
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_1", isProcessed = False))
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_2", isProcessed = False))
		print(lsc.upload_brand_operational_input_data(brand_name, "IMAGE_SET_3", isProcessed = False))

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
		logs = lsc.retreive_log_entities("input", "Patagonia/training", "Unprocessed")
		for entity in logs:
			print(" path [", entity['Path'],"] Processing Status: [", entity['Processing_Status'], "]")
		print("=====================================================")
		path = brand_name + "/operational"
		print("====================",path,"====================")
		logs = lsc.retreive_log_entities("input", "Patagonia/training", "Unprocessed")
		for entity in logs:
			print(" path [", entity['Path'],"] Processing Status: [", entity['Processing_Status'], "]")
		print("=====================================================")
# lsc.download_brand_training_input_data("Patagonia", processing_status_filter="Unprocessed")