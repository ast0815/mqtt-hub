# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class MQTTPlot(models.Model):
    """A plot of some MQTT data."""

    class Meta():
        verbose_name = "MQTT plot"
        verbose_name_plural = "MQTT plots"

    definition = models.TextField(default="")

