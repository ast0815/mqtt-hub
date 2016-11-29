"""Serializers for the use with rest-pandas"""

from rest_framework import serializers

from .models import MQTTMessage

import re
import copy

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MQTTMessage
        fields = ['id', 'time_recorded', 'topic', 'payload']
        pandas_index = ['id']

def generate_parsing_serializer_class(regex):
    """Generate a serializer class from a regular expression."""

    regex = re.compile(regex)
    groups = regex.groupindex.keys()

    # Copy vanilla MessageSerializer class
    class_name = 'DynamicParsingMessageSerializer'
    parent_classes = (MessageSerializer,)
    class_dict = {}

    meta_dict = copy.deepcopy(MessageSerializer.Meta.__dict__)
    class_dict['Meta'] = type('Meta', (object,), meta_dict)

    # Add additional parsed fields
    for group in groups:
        name, typ = MQTTMessage._parse_group_name(group)

        # Add custom field to the serializer
        class_dict['parsed_'+name] = serializers.SerializerMethodField()
        class_dict['Meta'].fields.append('parsed_'+name)

        # Add a method to actually get the value
        def _f(self, obj, name=name):
            parsed = obj.parse_payload(regex)
            if parsed is None or name not in parsed:
                return None
            else:
                return parsed[name]

        class_dict['get_parsed_'+name] = _f

    return type(class_name, parent_classes, class_dict)
