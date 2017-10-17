from django.shortcuts import render
from django.http import HttpResponse
from storage import AzureStorage



def index(request):
	#storage = AzureStorage()
	#return HttpResponse(storage.retrieve_table("patagonia"))
	#return HttpResponse("Hello, world! Time to detect some logos gang.")

	return render(request, 'detector/index.html', {"test": "Hello, world! Time to detect some logos gang."})

def operate(request, logo_id):
	storage = AzureStorage()
	'''
	for result in storage.retrieve_table("patagonia"):
		storage.download_blob(result.image_path)
	'''
	operate_results = storage.retrieve_table(logo_id)
	if operate_results is None:
		operate_results = "Invalid Table"
	operate_results_dict = {
		"operate_results": operate_results,
		"logo": logo_id
	}
	return render(request, 'detector/operate.html', operate_results_dict)

def operateForm(request):
	return render(request, 'detector/operateForm.html', {})
