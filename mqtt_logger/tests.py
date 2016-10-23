from django.test import TestCase, Client
from django.core.management import call_command
from django.core.urlresolvers import reverse
import urllib

from .models import *

class SubscriptionTests(TestCase):
    """General tests for the subscription models"""

    @classmethod
    def setUpTestData(cls):
        """Create an active and an inactive subscription."""

        activesub = MQTTSubscription(server='broker.hivemq.com', topic='mqtt-hub/tests/active')
        activesub.save()
        cls.activesub = activesub
        inactivesub = MQTTSubscription(server='broker.hivemq.com', topic='mqtt-hub/tests/inactive', active=False)
        inactivesub.save()
        cls.activesub = inactivesub

    def test_callback_function(self):
        """Test whether the callback function adds new messages."""

        sub = type(self).activesub

        # Create a message to save
        class ToyMessage():
            def __init__(self, topic, payload):
                self.topic = topic
                self.payload = payload

        test_topic = 'test'
        test_payload = '123abc'
        test_msg = ToyMessage(test_topic, test_payload)

        # Save the message using the callback function
        sub._record_message_callback(client=None, userdata=None, message=test_msg)

        # Get the newest message in the database and check for equality
        msg = MQTTMessage.objects.last()
        self.assertEqual(msg.topic, test_topic)
        self.assertEqual(msg.payload, test_payload)

    def test_connection(self):
        """Test whether one connection is established for each active subscription."""

        clients = MQTTSubscription.subscribe_all(start_loop=False)
        self.assertEqual(len(clients), 1)

class ListenerTests(TestCase):
    """Tests for the MQTT listener"""

    def setUp(self):
        """Create an active and an inactive subscription"""

        activesub = MQTTSubscription(server='broker.hivemq.com', topic='mqtt-hub/tests/active')
        activesub.save()
        self.activesub = activesub
        inactivesub = MQTTSubscription(server='broker.hivemq.com', topic='mqtt-hub/tests/inactive', active=False)
        inactivesub.save()
        self.inactivesub = inactivesub

    def test_listener_methods(self):
        """Test whether the subscription listener methods work."""

        activesub = self.activesub
        inactivesub = self.inactivesub

        MQTTSubscription.update_running_subscriptions()
        self.assertEqual(len(MQTTSubscription.running_subscriptions), 1)

        inactivesub.active = True
        inactivesub.save()

        MQTTSubscription.update_running_subscriptions()
        self.assertEqual(len(MQTTSubscription.running_subscriptions), 2)

        activesub.active = False
        activesub.save()

        MQTTSubscription.update_running_subscriptions()
        self.assertEqual(len(MQTTSubscription.running_subscriptions), 1)

        MQTTSubscription.stop_running_subscriptions()
        self.assertEqual(len(MQTTSubscription.running_subscriptions), 0)

class RESTTests(TestCase):
    """Tests for the REST API"""

    @classmethod
    def setUpTestData(cls):
        """Create a subscription, some messages and save the relevant URLs."""

        topic = 'mqtt-hub/tests'
        sub = MQTTSubscription(server='broker.hivemq.com', topic=topic)
        sub.save()
        cls.url = reverse('mqtt_logger:messages', kwargs={'topic': topic})
        for payload in ('_A_', '_B_', '_C_'):
            msg = MQTTMessage(subscription=sub, topic=topic, payload=payload)
            msg.save()
        for level in ('A', 'B', 'C'):
            topic = topic + '/' + level
            msg = MQTTMessage(subscription=sub, topic=topic, payload='_'+level+'_')
            msg.save()

    def setUp(self):
        """Create a client and other stuff that will be needed for view testing."""
        self.client = Client()

    def test_text_renderer(self):
        """Test the text renderer of the REST view."""

        client = self.client
        response = client.get(type(self).url, {'format': 'txt'})
        self.assertEqual(200, response.status_code)
        self.assertEqual('text/plain', response.accepted_media_type)
        self.assertIn('_A_', response.content)
        self.assertIn('_B_', response.content)
        self.assertIn('_C_', response.content)

    def test_csv_renderer(self):
        """Test the CSV renderer of the REST view."""

        client = self.client
        response = client.get(type(self).url, {'format': 'csv'})
        self.assertEqual(200, response.status_code)
        self.assertEqual('text/csv', response.accepted_media_type)
        self.assertIn('_A_', response.content)
        self.assertIn('_B_', response.content)
        self.assertIn('_C_', response.content)

    def test_json_renderer(self):
        """Test the JSON renderer of the REST view."""

        client = self.client
        response = client.get(type(self).url, {'format': 'json'})
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.accepted_media_type)
        self.assertIn('_A_', response.content)
        self.assertIn('_B_', response.content)
        self.assertIn('_C_', response.content)

    def test_limits(self):
        """Test whether `limit` and `skip` are working."""

        client = self.client
        url = type(self).url

        # Negative or garbage value should lead to defaul values
        response = client.get(url, {'skip': 'x', 'limit': 'x'})
        self.assertIn('_A_', response.content)
        self.assertIn('_B_', response.content)
        self.assertIn('_C_', response.content)

        response = client.get(url, {'skip': '-1', 'limit': '-1'})
        self.assertIn('_A_', response.content)
        self.assertIn('_B_', response.content)
        self.assertIn('_C_', response.content)

        # Only newest message should be returned
        response = client.get(url, {'limit': '1'})
        self.assertNotIn('_A_', response.content)
        self.assertNotIn('_B_', response.content)
        self.assertIn('_C_', response.content)

        # Second to newest
        response = client.get(url, {'skip': '1', 'limit': '1'})
        self.assertNotIn('_A_', response.content)
        self.assertIn('_B_', response.content)
        self.assertNotIn('_C_', response.content)

    def test_regex(self):
        """Test whether topic matching with '+' and '#' works."""

        client = self.client
        url = type(self).url + '/A'

        # First level should only contain the '_A_' message
        response = client.get(url)
        self.assertIn('_A_', response.content)
        self.assertNotIn('_B_', response.content)
        self.assertNotIn('_C_', response.content)

        # Second level should only contain the '_B_' message
        response = client.get(url+ '/+')
        self.assertNotIn('_A_', response.content)
        self.assertIn('_B_', response.content)
        self.assertNotIn('_C_', response.content)

        # Second and third level should contain the '_B_' and '_C_' messages
        response = client.get(url+ urllib.quote('/#'))
        self.assertNotIn('_A_', response.content)
        self.assertIn('_B_', response.content)
        self.assertIn('_C_', response.content)
