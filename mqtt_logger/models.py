from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import paho.mqtt.client as mqtt

class MQTTSubscription(models.Model):
    """Subscriptions define which MQTT messages are to be recorded."""

    server = models.CharField('Server name', max_length=200)
    topic = models.CharField('Topic subscribed to', max_length=1024)
    port = models.PositiveSmallIntegerField('Server port', default=1883)
    client_id = models.CharField('Client ID', max_length=1024, blank=True, default='')
    qos = models.PositiveSmallIntegerField('Quality of service', default=0, validators=[MaxValueValidator(2)])
    keep_alive = models.PositiveSmallIntegerField('Client timeout value', default=60)

    def _record_message_callback(self, client, userdata, message):
        """Save an MQTT message in the database.

        This is a callback functions to be used with `paho.mqtt.subscribe.callback`.
        """

        msg = MQTTMessage(subscription=self, topic=message.topic, payload=message.payload)
        msg.save()

    @classmethod
    def subscribe_all(klass, **kwargs):
        """Connect and subscribe to all subscriptions in the database."""

        clients = []
        for sub in klass.objects.all():
            clients.append(sub.subscribe(**kwargs))

        return clients

    def subscribe(self, start_loop=True):
        """Create a MQTT client and  subscribe to the server."""

        # Get client or create one
        try:
            client = self.mqtt_client
        except AttributeError:
            self.mqtt_client = mqtt.Client(client_id=self.client_id)
            client = self.mqtt_client

        client.on_message = self._record_message_callback
        client.connect(host=self.server, port=self.port, keepalive=self.keep_alive)
        client.subscribe(topic=self.topic, qos=self.qos)

        if start_loop:
            client.loop_start()

        # Add additional information to the client object
        client.host = self.server
        client.port = self.port
        client.topics = [self.topic]

        return client

    def __unicode__(self):
        return "%s: %s"%(self.server, self.topic)

class MQTTMessage(models.Model):
    """Base class to store all MQTT messages"""

    time_recorded = models.DateTimeField('Time recorded', auto_now_add=True, editable=False)
    subscription = models.ForeignKey(MQTTSubscription, on_delete=models.PROTECT, editable=False)
    topic = models.CharField('Topic', max_length=1024, editable=False)
    payload = models.TextField('Payload', max_length=16000, editable=False)

    def __unicode__(self):
        return "(%s) %s: %s"%(self.time_recorded, self.topic, self.payload[0:16])
