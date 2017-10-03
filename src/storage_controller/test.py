from storage_manager import LogoStorageConnector

lsc = LogoStorageConnector()

upload_demo = False
log_demo = True
download_demo = True
#"Puma", "Lego", "Nike", "Adidas", 
brand_names = ["patagonia"]

if(upload_demo == True):
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

if(log_demo == True):
	print("Demo for analyzing logs for multiple brands and their existing directories", brand_names)
	for brand_name in brand_names:
		path = brand_name + "/training"
		print("====================",path,"====================")
		unprocessed_logs = lsc.retreive_log_entities("input", "patagonia/training", "Unprocessed")
		for entity in unprocessed_logs:
			print(" prefix [", entity['Prefix'],"] Processing Status: [", entity['Processing_Status'], "]")
		processed_logs = lsc.retreive_log_entities("input", "patagonia/training", "Processed")
		for entity in processed_logs:
			print(" prefix [", entity['Prefix'],"] Processing Status: [", entity['Processing_Status'], "]")
		print("=====================================================")

		path = brand_name + "/operational"
		print("====================",path,"====================")
		unprocessed_logs = lsc.retreive_log_entities("input", "patagonia/operational", "Unprocessed")
		for entity in unprocessed_logs:
			print(" prefix [", entity['Prefix'],"] Processing Status: [", entity['Processing_Status'], "]")
		processed_logs = lsc.retreive_log_entities("input", "patagonia/operational", "Processed")
		for entity in processed_logs:
			print(" prefix [", entity['Prefix'],"] Processing Status: [", entity['Processing_Status'], "]")
		print("=====================================================")


if(download_demo == True):
	print("Demo for downloading data for multiple brands unprocessed input/operational data", brand_names)
	for brand_name in brand_names:	
		# blobs = lsc.download_brand_training_input_data(brand_name, processing_status_filter="Unprocessed")
		# for blob in blobs:
		# 	print("  blob name:",blob.name)
		# 	print("    blob content:",blob.content)
		blobs = lsc.download_brand_operational_input_data(brand_name, processing_status_filter="Unprocessed")
		for blob in blobs:
			print("  blob name:",blob.name)
			if(blob.content != None):
				print("    blob content:",len(blob.content))
			else:
				print("    could not download blob contents")