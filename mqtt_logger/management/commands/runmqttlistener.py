from django.core.management.base import BaseCommand, CommandError
from mqtt_logger.models import *


class Command(BaseCommand):
    help = 'Start listening to mqtt subscriptions and save messages in database.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write("Starting MQTT listener...")
        clients = MQTTSubscription.subscribe_all(start_loop=True)
        for c in clients:
            self.stdout.write("  %s:%s %s"%(c.host, c.port, c.topics))
        self.stdout.write("MQTT listener started.")
        self.stdout.write("Hit <ENTER> to quit.")
        wait = raw_input()

