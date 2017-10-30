from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'operateForm', views.operateForm, name='operateForm'),
    url(r'operate', views.operate, name='operate'),
    url(r'scrape', views.scrape, name='scrape'),
    url(r'csv', views.csv, name='csv'),
    url(r'callScraper', views.callScraper, name='callScraper'),
    url(r'train', views.train, name='train'),
    url(r'supload', views.supload, name='supload'),
    url(r'oupload', views.oupload, name='oupload'),
    url(r'oselect', views.oselect, name='oselect'),
    url(r'select', views.select, name='select'),
    url(r'upload', views.upload, name='upload'),


]
