from django.conf.urls import url

from .views import MessageView

app_name = 'mqtt_logger'

urlpatterns = [
    url(r'^messages/(?P<topic>.*)$', MessageView.as_view(), name='messages'),
]
