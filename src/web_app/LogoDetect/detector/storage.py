from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.base import ContentFile

import azure
from azure.storage import *
#from azure.storage.blob import BlockBlobService
from datetime import datetime
import os, mimetypes
from azure.cosmosdb.table import TableService, Entity

class AzureStorage(Storage):

    def __init__(self, container=None):
        self.table_service = TableService(account_name=settings.AZURE_STORAGE_ACCOUNT, account_key=settings.AZURE_STORAGE_KEY)
        '''
        self.storage_client = CloudStorageAccount(settings.AZURE_STORAGE_ACCOUNT, settings.AZURE_STORAGE_KEY)
        self.blob_service = self.storage_client.create_block_blob_service()
        if not container:
            self.container = "test container"
        else:
            self.container = container
        self.blob_service.create_container(
            self.container
            #public_access=PublicAccess.Blob
        )
        '''
        '''
        blob_service.create_blob_from_bytes(
            'mycontainername',
            'myblobname',
            b'<center><h1>Hello World!</h1></center>',
            content_settings=ContentSettings('text/html')
        )
        '''

        #print(blob_service.make_blob_url('mycontainername', 'myblobname'))
    def query(self, tableName, partitionKey, rowKey):
        task = self.table_service.get_entity(tableName, partitionKey, rowKey)
        return task.Availability

    def exists(self, name):
        try:
            self.blob_service.get_blob_properties(self.container, name)
            return True
        except:
            return False

