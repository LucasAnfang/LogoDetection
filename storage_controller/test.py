from storage_manager import LogoStorageConnector
lsc = LogoStorageConnector("IG_SCRAPER")

# lsc.upload_brand_training_input_data("Patagonia", "IMAGE_SET_1")
# lsc.upload_brand_training_input_data("Patagonia", "IMAGE_SET_2")
# lsc.upload_brand_training_input_data("Patagonia", "IMAGE_SET_3")
# lsc.upload_brand_training_input_data("Patagonia", "IMAGE_SET_4")

# lsc.upload_brand_operational_input_data("Patagonia", "IMAGE_SET_1")
# lsc.upload_brand_operational_input_data("Patagonia", "IMAGE_SET_2")

# lsc.upload_brand_operational_output_data("Patagonia", "IMAGE_SET_1")
# lsc.upload_brand_operational_output_data("Patagonia", "IMAGE_SET_2")

# lsc.upload_brand_training_input_data("Nike", "IMAGE_SET_1")
# lsc.upload_brand_training_input_data("Nike", "IMAGE_SET_2")
# lsc.upload_brand_training_input_data("Nike", "IMAGE_SET_3")
# lsc.upload_brand_training_input_data("Nike", "IMAGE_SET_4")

# lsc.upload_brand_operational_input_data("Nike", "IMAGE_SET_1")
# lsc.upload_brand_operational_input_data("Nike", "IMAGE_SET_2")

# lsc.upload_brand_operational_output_data("Nike", "IMAGE_SET_1")
# lsc.upload_brand_operational_output_data("Nike", "IMAGE_SET_2")
lsc.upload_brand_training_input_data("Patagonia", "Upload")
lsc.upload_brand_training_input_data("Patagonia", "Upload")
lsc.pretty_print_storage_structure()
# logs = lsc.retreive_log_entities("input", "Patagonia/training", "Upload")
# for entity in logs:
# 	print("Action ", entity['Action'], " interactor ", entity['Interacting_Entity'])
# lsc.download_brand_training_input_data("Patagonia")