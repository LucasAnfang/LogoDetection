from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../../'))
from src.instagram_scraper import IGScraperTool

@python_2_unicode_compatible  # only if you need to support Python 2
class BrandRequest(models.Model):
	brand = models.CharField(max_length = 50)
	max_images = models.PositiveIntegerField(default = 10)
	hashtag = models.CharField(max_length = 50)
	date = models.DateTimeField('Search Date')
	
	def __str__(self):
		return self.brand

	def save(self, *args, **kwargs):
		IGScraperTool.IG_train(self.brand, self.max_images)
		super(BrandRequest, self).save(*args, **kwargs)

@python_2_unicode_compatible  # only if you need to support Python 2
class TrainingUpload(models.Model):
	brand = models.CharField(max_length = 50)
	logo_directory_name = models.CharField(max_length = 50)
	no_logo_directory_name = models.CharField(max_length = 50)
	
	def __str__(self):
		return self.logo_directory_name

	def save(self, *args, **kwargs):
		IGScraperTool.IG_train_upload(brand, logo_directory_name, no_logo_directory_name)
		super(TrainingUpload, self).save(*args, **kwargs)

@python_2_unicode_compatible  # only if you need to support Python 2
class OperateForm(models.Model):
	brand = models.CharField(max_length = 50)
	
	def __str__(self):
		return self.brand

