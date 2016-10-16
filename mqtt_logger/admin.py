from django.contrib import admin

from models import *

class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ['subscription', 'time_recorded', 'topic', 'payload']

admin.site.register(MQTTMessage, MessageAdmin)

admin.site.register(MQTTSubscription)
