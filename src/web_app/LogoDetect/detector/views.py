from django.shortcuts import render
from django.http import HttpResponse
from storage import AzureStorage
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../../'))
from src.instagram_scraper import IGScraperTool



def index(request):
#	storage = AzureStorage(container="saracontainer")
#	return HttpResponse(storage.query("$MetricsHourPrimaryTransactionsBlob", "20171016T0000", "system;All"))
	return render(request, 'detector/index.html', {"test": "Logo Detection"})

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

def scrape(request):
	return render(request, 'detector/scrape.html', {})

def callScraper(request):
	if request.method == 'POST':
		if len(request.POST["brand"]) is 0 or len(request.POST["maxNum"]) is 0:
			return render(request, 'detector/scrape.html', {"errorString": "Please fill out both fields"})
		IGScraperTool.IG_train(request.POST["brand"], int(request.POST["maxNum"])+2)
	return render(request, 'detector/scrape.html', {"successString": "Pictures Scrapped!"})




