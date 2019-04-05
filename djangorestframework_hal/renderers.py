from urllib.parse import urlsplit
from collections import OrderedDict

from rest_framework.renderers import JSONRenderer
from rest_framework.settings import api_settings
from rest_framework.reverse import reverse

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def is_url(value):
    if not isinstance(value, str):
        return False
    try:
        URLValidator()(value)
    except ValidationError:
        return False
    return True


class HalJSONRenderer(JSONRenderer):
    media_type = "application/hal+json"

    @property
    def self_link_name(self):
        if api_settings.URL_FIELD_NAME:
            return api_settings.URL_FIELD_NAME
        else:
            return 'url'

    def get_url(self, renderer_context):
        # lookup_value = getattr(obj, self.lookup_field)
        # kwargs = {self.lookup_url_kwarg: lookup_value}
        # return self.reverse(view_name, kwargs=kwargs, request=request, format=format)
        view = renderer_context['view']

        if view.action in ('create', 'list'):
            action = 'list'
        else:
            action = 'detail'

        url = reverse(
            f'{view.basename}-{action}',
            args=renderer_context['args'],
            kwargs=renderer_context['kwargs'],
            request=renderer_context['request']
        )
        return url

    def get_view_name(self, renderer_context):
        return renderer_context['view'].basename

    def _render_dict(self, data, renderer_context):
        render_data = OrderedDict()

        link_data = OrderedDict()
        embedded_data = OrderedDict()

        for item, value in data.items():
            if is_url(value):
                if item == self.self_link_name:
                    item = 'self'
                link_data[item] = {'href': value}
            elif isinstance(value, dict):
                embedded_data[item] = self._render_dict(value, renderer_context)
            elif isinstance(value, list):
                embedded_data[item] = [self._render_dict(item, renderer_context) for item in data]
            else:
                render_data[item] = value
        if link_data:
            render_data['_links'] = link_data
            render_data.move_to_end('_links', last=False)
        if embedded_data:
            render_data['_embedded'] = embedded_data
        return render_data

    def render(self, data, accepted_media_type=None, renderer_context=None):
        render_data = OrderedDict()
        if isinstance(data, list):
            url = self.get_url(renderer_context)
            name = self.get_view_name(renderer_context)
            render_data['_links'] = {'self': {'href': url}}
            render_data['_embedded'] = {name: [self._render_dict(item, renderer_context) for item in data]}
        else:
            render_data = self._render_dict(data, renderer_context)

        res = super().render(render_data, accepted_media_type, renderer_context)
        return res

