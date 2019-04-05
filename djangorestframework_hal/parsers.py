from rest_framework.parsers import JSONParser

from .renderers import HalJSONRenderer


class HalJSONParser(JSONParser):
    # media_type = "application/hal+json"
    renderer_class = HalJSONRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type, parser_context)
        # print('before parse_data=', data)

        if not isinstance(data, dict):
            return data

        parsed_data = {}
        for item, value in data.items():
            if item == '_links':
                parsed_data.update({k: v['href'] for k, v in value.items()})

            elif item == '_embedded':
                #TODO
                pass
            else:
                parsed_data[item] = value

        # print('after parse_data=', parsed_data)
        return parsed_data
