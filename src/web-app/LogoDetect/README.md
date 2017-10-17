Anywhere:
> pip install Django==1.11

In web-app/LogoDetect/
> python manage.py runserver

In browser:
> http://127.0.0.1:8000/detector/

DB setup:
> https://docs.djangoproject.com/en/1.11/intro/tutorial02/

For azure table connection:
> pip install azure
> pip install azure-storage-blob
> pip install azure-storage-table
If that doesn't work, see https://github.com/Azure/azure-cosmosdb-python/tree/master/azure-cosmosdb-table for other options
