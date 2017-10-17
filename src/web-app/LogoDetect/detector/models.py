import azure
from azure.storage import *
from azure.storage.blob import BlockBlobService
from datetime import datetime
from azure.cosmosdb.table import TableService, Entity

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

@python_2_unicode_compatible  # only if you need to support Python 2
class BrandRequest(models.Model):
	brand = models.CharField(max_length = 50)
	max_images = models.PositiveIntegerField(default = 10)
	hashtag = models.CharField(max_length = 50)
	date = models.DateTimeField('Search Date')
	def __str__(self):
		return self.brand


class AzureTable(models.Model):
	table_service = TableService(account_name=settings.AZURE_STORAGE_ACCOUNT, account_key=settings.AZURE_STORAGE_KEY)
	blob_service = BlockBlobService(account_name=settings.AZURE_STORAGE_ACCOUNT, account_key=settings.AZURE_STORAGE_KEY)
	container = "input"
	table_list = [] #everything in the table for this logo
	logo = ""
	def retrieve_table(self, tableName):
		#tasks = table_service.query_entities(tableName, filter="PartitionKey eq 'tasksSeattle'", select='description')
		try:
			tasks = table_service.query_entities(tableName)
		except:
			return None
		logo = tableName
		for task in tasks:
			table_list.append(task)
		#sort it
		table_list = sorted(table_list, key=lambda k: k['has_logo']) 
		return table_list
    
