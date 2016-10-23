from django.shortcuts import render

from rest_pandas import PandasView
from rest_pandas.renderers import PandasCSVRenderer, PandasTextRenderer, PandasJSONRenderer
from .models import MQTTMessage
from .serializers import MessageSerializer

class MessageView(PandasView):
    """RESTful view to get a set of MQTT messages

    Named URL groups
    ----------------

    * `topic`   : This view will only return messages with a matching topic.

    Query strings
    -------------

    * `format`  : Set the file format to be returned. One of 'txt', 'csv', 'json'.
    * `limit`   : Limit the number of returned messages.
    * `skip`    : Skip the first N entries.

    """

    def get_queryset(self):
        """Get the queryset that will be rendered.

        The queryset is filtered by the topic as requested in the URL
        and optionally limited by the query string `limit=<n>`.
        A limit of 0 sets the limit to the maximum value.
        """

        topic = self.kwargs['topic']
        # Replace '+' and '#' with standard regular expression
        topic = topic.replace(r'+', r'[^/]*')
        topic = topic.replace(r'#', r'.*')
        topic = r'^' + topic + r'$'

        default_limit = 100
        max_limit = 1000
        limit = self.request.GET.get('limit', default_limit)
        try:
            limit = int(limit)
        except ValueError:
            limit = default_limit
        if limit < 1 or limit > max_limit:
            limit = max_limit

        skip = self.request.GET.get('skip', 0)
        try:
            skip = int(skip)
        except ValueError:
            skip = 0
        if skip < 0:
            skip = 0

        return MQTTMessage.objects.filter(topic__regex=topic).order_by('-time_recorded')[skip:skip+limit]

    serializer_class = MessageSerializer
    renderer_classes = [PandasCSVRenderer, PandasTextRenderer, PandasJSONRenderer]
