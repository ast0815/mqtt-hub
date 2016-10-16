from django.test import TestCase

from models import *

class SubscriptionTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        sub = MQTTSubscription(server='localhost', topic='#')
        sub.save()
        cls.sub = sub

    def test_callback_function(self):
        sub = type(self).sub

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
