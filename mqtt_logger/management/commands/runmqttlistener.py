from django.core.management.base import BaseCommand, CommandError
from mqtt_logger.models import *

import time

class Command(BaseCommand):
    help = 'Start listening to mqtt subscriptions and save messages in database.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write("Starting MQTT listener...")
        subs = list(MQTTSubscription.objects.filter(active=True))
        for s in subs:
            self.stdout.write("  Connecting to %s:%s %s"%(s.server, s.port, s.topic))
            s.client = s.subscribe(start_loop=True)
        while(True):
            time.sleep(10)
            newsubs = MQTTSubscription.objects.filter(active=True)
            for s in subs:
                if s not in newsubs:
                    self.stdout.write("  Disconnecting from %s:%s %s"%(s.server, s.port, s.topic))
                    s.client.disconnect()
                    subs.remove(s)
            for s in newsubs:
                if s not in subs:
                    self.stdout.write("  Connecting to %s:%s %s"%(s.server, s.port, s.topic))
                    s.client = s.subscribe(start_loop=True)
                    subs.append(s)
