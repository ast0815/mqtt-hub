from django.conf import settings as global_settings

class Defaults():
    MQTT_PLOTTER_USE_JSDELIVR = False

class MQTTSettings(object):
    """Handle settings with proper defaults."""

    def __getattr__(self, attr):
        try:
            return getattr(global_settings, attr)
        except AttributeError:
            return getattr(Defaults, attr)

settings = MQTTSettings()
