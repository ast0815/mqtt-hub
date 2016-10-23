from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from .models import *

class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('subscription_link', 'time_recorded', 'topic', 'payload')
    date_hierarchy = 'time_recorded'
    list_display = ('time_recorded', 'subscription', 'topic', 'payload')
    list_display_links = ('payload',)
    list_filter = ('subscription', 'time_recorded', 'topic')
    ordering = ('-time_recorded',)

    def subscription_link(self, obj):
        """Return the link to the MQTTSubscription object admin page."""

        url = reverse('admin:%s_%s_change' %(obj.subscription._meta.app_label,  obj.subscription._meta.model_name),  args=[obj.subscription.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.subscription))

    subscription_link.short_description = "MQTT subscription"

admin.site.register(MQTTMessage, MessageAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('server', 'topic', 'active')
    list_editable = ('active',)
    list_filter = ('server', 'active')
    ordering = ('server', 'topic')

admin.site.register(MQTTSubscription, SubscriptionAdmin)
