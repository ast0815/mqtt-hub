from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import paho.mqtt.client as mqtt
import re

class MQTTSubscription(models.Model):
    """Subscriptions define which MQTT messages are to be recorded."""

    class Meta():
        verbose_name = "MQTT subscription"
        verbose_name_plural = "MQTT subscriptions"

    server = models.CharField('Server name', max_length=200)
    topic = models.CharField('Topic subscribed to', max_length=1024)
    port = models.PositiveSmallIntegerField('Server port', default=1883)
    client_id = models.CharField('Client ID', max_length=1024, blank=True, default='')
    qos = models.PositiveSmallIntegerField('Quality of service', default=0, validators=[MaxValueValidator(2)])
    keep_alive = models.PositiveSmallIntegerField('Client timeout value', default=60)
    active = models.BooleanField('Active', default=True)

    def _record_message_callback(self, client, userdata, message):
        """Save an MQTT message in the database.

        This is a callback functions to be used with `paho.mqtt.subscribe.callback`.
        """

        msg = MQTTMessage(subscription=self, topic=message.topic, payload=message.payload)
        msg.save()

    running_subscriptions = []

    @classmethod
    def update_running_subscriptions(cls):
        """Connect to all active subscription and disconnect from inactive ones."""

        newsubs = cls.objects.filter(active=True)

        # Disconnect from inactive subs
        for s in cls.running_subscriptions:
            if s not in newsubs:
                s.client.disconnect()
                cls.running_subscriptions.remove(s)

        # Connect to active subs
        for s in newsubs:
            if s not in cls.running_subscriptions:
                s.client = s.subscribe(start_loop=True)
                cls.running_subscriptions.append(s)

    @classmethod
    def stop_running_subscriptions(cls):
        """Stop all running subscrptions."""

        for s in cls.running_subscriptions:
            s.client.disconnect()

        cls.running_subscriptions = []

    @classmethod
    def subscribe_all(cls, **kwargs):
        """Connect and subscribe to all subscriptions in the database."""

        clients = []
        for sub in cls.objects.filter(active=True):
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
        if self.active:
            return "%s: %s"%(self.server, self.topic)
        else:
            return "[%s: %s]"%(self.server, self.topic)

class MQTTMessage(models.Model):
    """Base class to store all MQTT messages"""

    class Meta():
        verbose_name = "MQTT message"
        verbose_name_plural = "MQTT messages"

    time_recorded = models.DateTimeField('Time recorded', auto_now_add=True, editable=False)
    subscription = models.ForeignKey(MQTTSubscription, on_delete=models.PROTECT, editable=False)
    topic = models.CharField('Topic', max_length=1024, editable=False)
    payload = models.TextField('Payload', max_length=16000, editable=False)

    def search_payload(self, regex):
        """Search the payload and extract variables from it.

        Uses `re.search` and returns `MatchObject` or `None`.
        """

        return re.search(regex, self.payload)

    @staticmethod
    def _parse_group_name(group_name):
        """Parse the name of a named group for payload parsing.

        Returns (name, type).
        """

        type_match = re.match('([dieEfgs])_(.+)', group_name)
        if type_match is None:
            type_char = 's'
        else:
            type_char = type_match.group(1)
            group_name = type_match.group(2)

        if type_char in 'di':
            # Integer
            typ = int
        elif type_char in 'eEfg':
            # Float
            typ = float
        elif type_char in 's':
            # String, no parsing needed
            typ = str
        else:
            raise ValueError("Unknown type character <%s>. This should never happen!"%(type_char,))

        return (group_name, typ)

    def parse_payload(self, regex):
        """Parse the payload into a dict of variables.

        The `regex` should contain at least one named group of the form `(?P<d_name>[-+]?\d+)`.
        The first letter (before the '_') decides how the matched string is interpreted:

            d,i:        int(match)
            e,E,f,g:    float(match)
            s           string, i.e. no interpretation

        Named groups that do not start with the 'd_' form are interpreted as strings.

        Returns `None` if the regex does not match, otherwise the dict of the interpreted groups.
        """

        match = self.search_payload(regex)
        if match is None:
            return None

        ret = {}
        groups = match.groupdict()

        for key in groups:

            group_name, typ = type(self)._parse_group_name(key)

            try:
                ret[group_name] = typ(groups[key])
            except ValueError:
                ret[group_name] = None

        return ret

    def __unicode__(self):
        return "(%s) %s: %s"%(self.time_recorded, self.topic, self.payload[0:16])
