from django.conf.urls import url

from .views import *

app_name = 'mqtt_plots'

urlpatterns = [
    url(r'simple/(?P<id>[0-9]+)/', SimplePlotView.as_view(), name='simple'),
    url(r'spec/(?P<id>[0-9]+)/', definition, name='definition'),
]
