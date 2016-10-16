# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 14:17
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MQTTMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_recorded', models.DateTimeField(auto_now_add=True, verbose_name='Time recorded')),
                ('payload', models.TextField(max_length=16000, verbose_name='Payload')),
                ('topic', models.CharField(max_length=1024, verbose_name='Topic')),
            ],
        ),
        migrations.CreateModel(
            name='MQTTSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server', models.CharField(max_length=200, verbose_name='Server name')),
                ('topic', models.CharField(max_length=1024, verbose_name='Topic subscribed to')),
                ('port', models.PositiveSmallIntegerField(default=1883, verbose_name='Server port')),
                ('client_id', models.CharField(blank=True, default='', max_length=1024, verbose_name='Client ID')),
                ('qos', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(2)], verbose_name='Quality of service')),
                ('keep_alive', models.PositiveSmallIntegerField(default=60, verbose_name='Client timeout value')),
            ],
        ),
        migrations.AddField(
            model_name='mqttmessage',
            name='subscription',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='mqtt_logger.MQTTSubscription'),
        ),
        migrations.AlterField(
            model_name='mqttmessage',
            name='payload',
            field=models.TextField(editable=False, max_length=16000, verbose_name='Payload'),
        ),
        migrations.AlterField(
            model_name='mqttmessage',
            name='topic',
            field=models.CharField(editable=False, max_length=1024, verbose_name='Topic'),
        ),
    ]
