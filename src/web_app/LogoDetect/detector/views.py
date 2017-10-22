from django.shortcuts import render
from django.http import HttpResponse
from storage import AzureStorage
import sys
import os
import shutil
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
	if request.method == 'POST':
		if len(request.POST["picList"]) is 0:
			return render(request, 'detector/trainSelect.html', {"errorString": "Please input a brand"})

	pathList = request.POST["picList"].split(',')
	nonPathList = request.POST["nonPicList"].split(',')
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
	#IGScraperTool.IG_train_upload(request.POST["brand"].lower(), logoDir, noLogoDir)
	shutil.rmtree("no"+request.POST["brand"])
	shutil.rmtree("yes"+request.POST["brand"])
	shutil.rmtree(request.POST["brand"])
	return render(request, 'detector/trainSelect.html', {"output": "Training Session Started"})




def oupload(request):
	if request.method == 'POST':
		if len(request.POST["brand"]) is 0 or len(request.POST["maxNum"]) is 0 or len(request.POST["hashtagList"]) is 0:
			return render(request, 'detector/operateSelect.html', {"errorString": "Please fill out all fields"})
	print request.POST["hashtagList"]
	htList = request.POST["hashtagList"].split(',')
	#IGScraperTool.IG_operate(request.POST["brand"].lower(), htList, request.POST["maxNum"]):
	return render(request, 'detector/operateSelect.html', {"output": "Operate Session Started"})

def upload(request):
	if request.method == 'POST':
		if len(request.POST["brand"]) is 0 or len(request.POST["logoNoDir"]) is 0 or len(request.POST["logoDir"]) is 0:
			return render(request, 'detector/train.html', {"errorString": "Please fill out all fields"})
	#IGScraperTool.IG_train_upload(request.POST["brand"], request.POST["logoDir"], request.POST["logoNoDir"])
	return render(request, 'detector/train.html', {"successString": "Testing mode but worked!"})
