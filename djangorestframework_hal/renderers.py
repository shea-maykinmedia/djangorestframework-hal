from rest_framework.reverse import reverse

from .settings import api_settings
from .utils import transform_from_json_to_hal


class HalJSONRenderer(api_settings.RENDERER_CLASS):
    media_type = "application/hal+json"

    @staticmethod
    def get_url(renderer_context):
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

    @staticmethod
    def get_view_name(renderer_context):
        return renderer_context['view'].basename

    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        response = renderer_context.get('response')

        # if we have an error, return data as-is
        if response is not None and response.status_code >= 400:
            return super().render(data, accepted_media_type, renderer_context)

        url = self.get_url(renderer_context)
        name = self.get_view_name(renderer_context)

        render_data = transform_from_json_to_hal(data, url, name)

        res = super().render(render_data, accepted_media_type, renderer_context)
        return res
