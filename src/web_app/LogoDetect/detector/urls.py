from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'operateForm', views.operateForm, name='operateForm'),
    url(r'scrape', views.scrape, name='scrape'),
    url(r'callScraper', views.callScraper, name='callScraper'),
    url(r'train', views.train, name='train'),
    url(r'select', views.select, name='select'),
    url(r'upload', views.upload, name='upload'),
    url(r'^(?P<logo_id>[^\s]+)/operate/$', views.operate, name='operate'),
 
]