from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'operateForm', views.operateForm, name='operateForm'),
    #url(r'operateForm', views.operateForm, name='operateForm'),
    url(r'^(?P<logo_id>[^\s]+)/operate/$', views.operate, name='operate'),
]