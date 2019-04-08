from django.conf import settings

from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, "HAL_JSON", {})

DEFAULTS = {
    "RENDERER_CLASS": "rest_framework.renderers.JSONRenderer",
    "PARSER_CLASS": "rest_framework.parsers.JSONParser",
}

IMPORT_STRINGS = ("RENDERER_CLASS", "PARSER_CLASS")


api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
