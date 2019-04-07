from collections import OrderedDict
from typing import Union

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

Primitive = Union[str, float, int, bool, None]


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


def transform_dict(json_dict) -> Embedded:
    links = OrderedDict() 
    embedded = OrderedDict()
    data = OrderedDict()

    for k, v in json_dict.items():
        transformed = transform_token(v)
        
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


def transform_list(tokens) -> Embedded:
    return Embedded([unpack(transform_token(token)) for token in tokens])


def transform_str(string: str) -> Union[Link, str]:
    if is_url(string):
        return Link(string)
    return string


def transform_token(token) -> Union[Embedded, Link, Primitive]:
    if isinstance(token, str):
        return transform_str(token)

    if isinstance(token, list):
        return transform_list(token)

    if isinstance(token, dict):
        return transform_dict(token)

    # value primitives: int, float, bool, None
    return token


def transform(data, url: str, name: str) -> Union[OrderedDict, Primitive]:
    token = data
    if isinstance(data, list):
        token = {
            'url': url,
            name: data
        }

    transformed = transform_token(token)
    return unpack(transformed)
