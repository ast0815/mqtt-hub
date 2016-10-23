from django.core.management.base import BaseCommand, CommandError
from mqtt_logger.models import *

import time

class Command(BaseCommand):
    help = 'Start listening to mqtt subscriptions and save messages in database.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write("Starting MQTT listener...")
        self.stdout.write("Quit with CTRL-C.")
        try:
            while(True):
                MQTTSubscription.update_running_subscriptions()
                time.sleep(10)
        except KeyboardInterrupt:
            self.stdout.write("Quitting...")
            MQTTSubscription.stop_running_subscriptions()
