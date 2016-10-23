mqtt-hub
========

[![Build Status](https://travis-ci.org/ast0815/mqtt-hub.svg?branch=master)](https://travis-ci.org/ast0815/mqtt-hub)
[![Coverage Status](https://coveralls.io/repos/github/ast0815/mqtt-hub/badge.svg?branch=master)](https://coveralls.io/github/ast0815/mqtt-hub?branch=master)

A web interface and logger for MQTT, based on Django

Usage
-----

The admin interface can be tested by running `./managy.py runserver`.

The connection to actual MQTT brokers works by adding subscriptions to the database and then starting the listener.

    $ .\manage.py runmqttlistener

Messages send over brokers in topics that were subscribed to should now be saved in the database.

The messages can be accessed via a REST API:

    http://localhost:8000/mqtt/messages/topic/you/want?format=txt&limit=5&skip=0

The `format` must be one of 'txt', 'csv', 'json'.
