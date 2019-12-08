# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

# Create your models here.
class MQTTPlot(models.Model):
    """A plot of some MQTT data."""

    class Meta():
        verbose_name = "MQTT plot"
        verbose_name_plural = "MQTT plots"

    definition = models.TextField(default="")

    def simple_url(self):
        """Return the url to the simple plot page."""
        return reverse('mqtt_plotter:simple', kwargs={'id': self.id})
