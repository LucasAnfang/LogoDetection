from django.shortcuts import render
from django.http import HttpResponse
from storage import AzureStorage


def index(request):
	storage = AzureStorage(container="saracontainer")
	return HttpResponse(storage.query("$MetricsHourPrimaryTransactionsBlob", "20171016T0000", "system;All"))
	return HttpResponse("Hello, world! Time to detect some logos gang.")