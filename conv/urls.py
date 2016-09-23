from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^conv$', views.convert, name='converter'),
    url(r'^conv/getconf.py$', views.get_conf, name='config_files'),
    url(r'^conv/getprev.py$', views.get_prev, name='config_files_prev'),
    url(r'^load$', views.load, name='load'),
    url(r'^conv/getpage.py$', views.get_page, name='getpage'),
    url(r'^conv/getfile$', views.get_file, name='getpage'),
    url(r'^conv/getconftable$', views.getconftable, name='getconftable')
]
