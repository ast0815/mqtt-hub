mqtt-hubi [![Build Status](https://travis-ci.org/ast0815/mqtt-hub.svg?branch=master)](https://travis-ci.org/ast0815/mqtt-hub)
========

A web interface and logger for MQTT, based on Django

Usage
-----

The admin interface can be tested by running `./managy.py runserver`.

The connection to actual MQTT brokers works by adding subscriptions to the database and then starting the subscription loops.

    $ .\manage.py shell

    In [1]: from mqtt_logger.models import *

    In [2]: clients = MQTTSubscription.subscribe_all()

Messages send over brokers in topics that were subscribed to should now be saved in the database.
