from django.shortcuts import render
from django.http import HttpResponse
import sys
import os
import shutil
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../../'))
from src.instagram_scraper import IGScraperTool
from src.storage_controller.storage import AzureStorage




def index(request):
#	storage = AzureStorage(container="saracontainer")
#	return HttpResponse(storage.query("$MetricsHourPrimaryTransactionsBlob", "20171016T0000", "system;All"))
	return render(request, 'detector/index.html', {"test": "Logo Detection"})

def csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
	import csv
	if request.method == 'GET':
		print "here!"
		print request.GET['brand']
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="'+request.GET.get('brand')+'.csv"'

		storage = AzureStorage()
		operate_results = storage.retrieve_table(request.GET.get('brand'))
		keys = operate_results[0].keys()
		writer = csv.DictWriter(response, keys)
		writer.writeheader()
		writer.writerows(operate_results)
		return response


def operate(request):
	if request.method == 'POST':
		print "in operate"
		print request.POST
		if len(request.POST.get('brand')) is 0:
			return render(request, 'detector/operateForm.html', {"errorString": "Please fill out both fields"})

		storage = AzureStorage()
		logo_id = request.POST.get('brand')
		print logo_id
		operate_results = storage.retrieve_table(logo_id)
		if operate_results is None:
			operate_results = "Invalid Table"
			operate_results_dict = {
				"operate_results": operate_results,
				"logo": logo_id
			}
			return render(request, 'detector/operate.html', operate_results_dict)
		#dict: id to of list for context
		operate_results_dict = {
			"operate_results": operate_results,
			"logo": logo_id
		}
		'''
		for item in operate_results:
			operate_results_dict[item.PartitionKey] = item.context

		print operate_results[0].image_context
		print type(operate_results[0].image_context)
		'''
		return render(request, 'detector/operate.html', operate_results_dict)

def operateForm(request):
	return render(request, 'detector/operateForm.html', {})

def scrape(request):
	return render(request, 'detector/scrape.html', {})

def callScraper(request):
	if request.method == 'POST':
		if len(request.POST["brand"]) is 0 or len(request.POST["maxNum"]) is 0:
			return render(request, 'detector/scrape.html', {"errorString": "Please fill out both fields"})
		IGScraperTool.IG_train(request.POST["brand"].lower(), int(request.POST["maxNum"])+3)
	return render(request, 'detector/scrape.html', {"successString": "Pictures Scraped!"})

def train(request):
	print "here"
	return render(request, 'detector/train.html', {})

def oselect(request):
	return render(request, 'detector/operateSelect.html', {})

def select(request):
	if request.method == 'POST':
		if len(request.POST["brand"]) is 0:
			return render(request, 'detector/train.html', {"errorString": "Please input a brand"})
		brand = request.POST["brand"].lower()
		if not os.path.isdir(brand):
			errStr = "There are no pictures currently saved for " + brand+". Please scrape some picture from Instagram"
			return render(request, 'detector/train.html', {"errorString": errStr})
		picList = os.listdir(brand)
		picPathList = []
		for pic in picList:
			picPathList.append('/'+brand+'/'+ pic)
		resultDict = {
			"logo" : brand,
			"picList": picPathList,
		}
	return render(request, 'detector/trainSelect.html', resultDict)

def supload(request):
	print "in supload"
	if request.method == 'POST':
		if len(request.POST["picList"]) is 0:
			return render(request, 'detector/trainSelect.html', {"errorString": "Please input a brand"})
		pathList = request.POST["picList"].split(',')
		nonPathList = request.POST["nonPicList"].split(',')
		brandName = request.POST["brand"]
		if request.POST["logoName"] is not "":
			brandName = request.POST["logoName"]
		if not os.path.isdir("no"+request.POST["brand"]):
			os.makedirs("no"+request.POST["brand"])
		if not os.path.isdir("yes"+request.POST["brand"]):
			os.makedirs("yes"+request.POST["brand"])
		for goodPath in pathList:
			newPath = "yes"+request.POST["brand"]+"/"+goodPath.split('/')[len(goodPath.split('/'))-1]
			try:
				os.rename(goodPath, newPath)
			except:
				print "error"
		for badPath in nonPathList:
			newPath = "no"+request.POST["brand"]+"/"+badPath.split('/')[len(badPath.split('/'))-1]
			try:
				os.rename(goodPath, newPath)
			except:
				print "error"
		logoDir = os.getcwd() + "/" + "yes"+request.POST["brand"]
		noLogoDir = os.getcwd() + "/" + "no"+request.POST["brand"]
		print "made it to before tool"
		IGScraperTool.IG_train_upload(brandName.lower(), logoDir, noLogoDir)
		print "made it after tools"
		shutil.rmtree("no"+request.POST["brand"])
		shutil.rmtree("yes"+request.POST["brand"])
		shutil.rmtree(request.POST["brand"])
		return render(request, 'detector/trainSelect.html', {"output": "Training Session Started"})




def oupload(request):
	if request.method == 'POST':
		if len(request.POST["brand"]) is 0 or len(request.POST["maxNum"]) is 0 or len(request.POST["hashtagList"]) is 0:
			return render(request, 'detector/operateSelect.html', {"errorString": "Please fill out all fields"})
		print request.POST["maxNum"]
		htList = request.POST["hashtagList"].split(',')
		print str(htList)
		IGScraperTool.IG_operate(request.POST["brand"].lower(), htList, request.POST["maxNum"])
		print "after scraper tool"
		return render(request, 'detector/operateSelect.html', {"output": "Operate Session Started"})

def upload(request):
	if request.method == 'POST':
		if len(request.POST["brand"]) is 0 or len(request.POST["logoNoDir"]) is 0 or len(request.POST["logoDir"]) is 0:
			return render(request, 'detector/train.html', {"errorString": "Please fill out all fields"})
	IGScraperTool.IG_train_upload(request.POST["brand"], request.POST["logoDir"], request.POST["logoNoDir"])
	return render(request, 'detector/train.html', {"successString": "Testing mode but worked!"})
