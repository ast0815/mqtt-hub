# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.html import format_html
from . import models

# Register your models here.
class PlotAdmin(admin.ModelAdmin):
    readonly_fields = ('simple_link',)

    def simple_link(self, instance):
        """Return a link to the simple view."""
        url = instance.simple_url()
        return format_html('<a href="{0}" target="_blank">{1}</a>', url, url)

admin.site.register(models.MQTTPlot, PlotAdmin)
