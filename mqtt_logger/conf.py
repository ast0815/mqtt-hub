from django.conf import settings as global_settings

class Defaults():
    MQTT_LOGGER_TEMPLATE = 'mqtt_logger/messages.html'

class MQTTSettings(object):
    """Handle settings with proper defaults."""

    def __getattr__(self, attr):
        try:
            return getattr(global_settings, attr)
        except AttributeError:
            return getattr(Defaults, attr)

settings = MQTTSettings()
