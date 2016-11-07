mqtt-hub
========

[![Build Status](https://travis-ci.org/ast0815/mqtt-hub.svg?branch=master)](https://travis-ci.org/ast0815/mqtt-hub)
[![Coverage Status](https://coveralls.io/repos/github/ast0815/mqtt-hub/badge.svg?branch=master)](https://coveralls.io/github/ast0815/mqtt-hub?branch=master)
[![Requirements Status](https://requires.io/github/ast0815/mqtt-hub/requirements.svg?branch=master)](https://requires.io/github/ast0815/mqtt-hub/requirements/?branch=master)

A web interface and logger for MQTT, based on Django

Usage
-----

The admin interface can be tested by running `./managy.py runserver`.

The connection to actual MQTT brokers works by adding subscriptions to the database and then starting the listener.

    $ .\manage.py runmqttlistener

Messages send over brokers in topics that were subscribed to should now be saved in the database.

The messages can be accessed via a REST API:

    http://localhost:8000/mqtt/messages/topic/you/want?format=txt&limit=5&skip=0&parse=<regex>

The `format` must be one of 'txt', 'csv', 'json'.
The message payloads can optionally be parsed with a regular expression provided with the `parse` argument.
It accepts standard Python regular expressions.
All *named* groups in the expression will ne added as additional columns to the output data.
If a group's name starts with one of the following letters and an underscore '_', the group is interpreted as that data type:

    d,i:        int(match)
    e,E,f,g:    float(match)
    s:          string, i.e. no interpretation

For example, the group `(?P<d_number>\d+)` would be interpreted as an integer and a column 'parsed_number' would be added to the output data.
