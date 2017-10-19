from django.contrib import admin
from .models import BrandRequest
from .models import TrainingUpload
from .models import OperateForm

admin.site.register(BrandRequest)

admin.site.register(TrainingUpload)

admin.site.register(OperateForm)

