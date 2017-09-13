from storage_manager import LogoStorageConnector
lsc = LogoStorageConnector()

lsc.upload_brand_training_input_data("Patagonia", "Hat")
# lsc.upload_brand_training_input_data("Patagonia", "fun")

# lsc.upload_brand_operational_input_data("Patagonia", "Shirt with logo")
# lsc.upload_brand_operational_input_data("Patagonia", "Star Wars")

# lsc.upload_brand_operational_output_data("Patagonia", "Star Wars Rules")
# lsc.upload_brand_operational_output_data("Patagonia", "Star Trek Drules")

lsc.pretty_print_storage_structure()
lsc.download_brand_training_input_data("Patagonia")