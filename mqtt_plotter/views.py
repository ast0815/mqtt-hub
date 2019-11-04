# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from .conf import settings
from django.http import HttpResponse
from .models import *

class SimplePlotView(TemplateView):
    template_name = "mqtt_plotter/simple_view.html"

    def get_context_data(self, **kwargs):
        context = super(SimplePlotView, self).get_context_data(**kwargs)
        context['settings'] = settings
        context['plot'] = MQTTPlot.objects.get(id=kwargs.get('id', None))
        return context

def definition(request, **kwargs):
    js = MQTTPlot.objects.get(id=kwargs.get('id', None)).definition
    resp = HttpResponse(js)
    resp['Content-Type'] = 'application/json'
    return resp
