from django.contrib import admin

from .models import *

class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('subscription', 'time_recorded', 'topic', 'payload')
    date_hierarchy = 'time_recorded'
    list_display = ('time_recorded', 'subscription', 'topic', 'payload')
    list_display_links = ('payload',)
    list_filter = ('subscription', 'time_recorded', 'topic')
    ordering = ('-time_recorded',)

admin.site.register(MQTTMessage, MessageAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('server', 'topic', 'active')
    list_editable = ('active',)
    list_filter = ('server', 'active')
    ordering = ('server', 'topic')

admin.site.register(MQTTSubscription, SubscriptionAdmin)
