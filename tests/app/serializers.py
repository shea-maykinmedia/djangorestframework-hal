from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from .models import Author, Book


class AuthorUrlSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('url', 'name', 'email')
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }


class BookUrlSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('url', 'title', 'pages', 'author')
        expandable_fields = {
            'author': AuthorUrlSerializer
        }
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
            'author': {
                'lookup_field': 'uuid',
            }
        }
