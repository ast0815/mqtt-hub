# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
class PlotAdmin(admin.ModelAdmin):
    pass
    #list_display = ('server', 'topic', 'active')
    #list_editable = ('active',)
    #list_filter = ('server', 'active')
    #ordering = ('server', 'topic')

admin.site.register(MQTTPlot, PlotAdmin)
