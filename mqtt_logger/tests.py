from django.test import TestCase

from models import *

class SubscriptionTests(TestCase):

    @classmethod
    def setUpTestData(cls):
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
