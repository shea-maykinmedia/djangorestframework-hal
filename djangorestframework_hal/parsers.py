from .renderers import HalJSONRenderer
from .settings import api_settings
from .utils import parse_from_hal


class HalJSONParser(api_settings.PARSER_CLASS):
    media_type = "application/hal+json"
    renderer_class = HalJSONRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type, parser_context)

        parsed_data = parse_from_hal(data)
        return parsed_data
