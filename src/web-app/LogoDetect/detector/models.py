from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class BrandRequest(models.Model):
	brand = models.CharField(max_length = 50)
	max_images = models.PositiveIntegerField(default = 10)
	hashtag = models.CharField(max_length = 50)
	date = models.DateTimeField('Search Date')
	def __str__(self):
		return self.brand
