# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-04 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mqtt_plotter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mqttplot',
            name='definition',
            field=models.TextField(default=''),
        ),
    ]
