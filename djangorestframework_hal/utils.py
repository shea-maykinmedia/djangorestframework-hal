from collections import OrderedDict
from typing import Union

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

Primitive = Union[str, float, int, bool, None]


# for renderer
class Link:
    def __init__(self, link):
        self.link = link


class Embedded:
    def __init__(self, embedded):
        self.embedded = embedded


def is_url(value):
    if not isinstance(value, str):
        return False
    try:
        URLValidator()(value)
    except ValidationError:
        return False
    return True


def unpack(transformed: Union[Embedded, Link, Primitive]) -> Union[OrderedDict, list, Primitive]:
    if isinstance(transformed, Embedded):
        return transformed.embedded
    if isinstance(transformed, Link):
        return transformed.link
    return transformed


def render_dict(json_dict, paginated=False) -> Embedded:
    links = OrderedDict() 
    embedded = OrderedDict()
    data = OrderedDict()

    for k, v in json_dict.items():
        #if empty string and pagination - move them to _links
        if paginated \
                and k in ('next', 'previous', 'first', 'last')\
                and v is None:
            transformed = Link(v)
        else:
            transformed = render_token(v)
        
        if isinstance(transformed, Link):
            links[k] = {'href': transformed.link}
        elif isinstance(transformed, Embedded):
            embedded[k] = transformed.embedded
        else:
            data[k] = v

    if 'url' in links:
        links['self'] = links.pop('url')

    transformed_dict = OrderedDict()
    if links:
        transformed_dict['_links'] = links
    if embedded:
        transformed_dict['_embedded'] = embedded
    
    transformed_dict.update(data)

    return Embedded(transformed_dict)


def render_list(json_list) -> Embedded:
    return Embedded([unpack(render_token(token)) for token in json_list])


def render_str(string) -> Union[Link, str]:
    if is_url(string):
        return Link(string)
    return string


def render_token(token, paginated=False) -> Union[Embedded, Link, Primitive]:
    if isinstance(token, str):
        return render_str(token)

    if isinstance(token, list):
        return render_list(token)

    if isinstance(token, dict):
        return render_dict(token, paginated)

    # value primitives: int, float, bool, None
    return token


# for parser
def parse_from_hal(data):
    if not isinstance(data, dict):
        return data

    parsed_data = {}
    for item, value in data.items():
        if item == '_links':
            link_data = {k: v['href'] for k, v in value.items() if k != 'self'}
            parsed_data.update(link_data)

        elif item == '_embedded':
            embedded_data = {k: parse_from_hal(v) for k, v in value.items()}
            parsed_data.update(embedded_data)
        else:
            parsed_data[item] = value

    return parsed_data
