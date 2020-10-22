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


class AuthorUrlSerializerWithCustomLink(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('url', 'name', 'email')
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }

    def to_representation(self, *args, **kwargs):
        representation = super().to_representation(*args, **kwargs)

        representation['books_links'] = []
        for author in self.instance:
            for book in author.book_set.all().order_by('-pages'):
                representation['books_links'].append({
                    'url': f'http://localhost/author_hal/{author.uuid}/books_hal/{book.uuid}'
                })

        return representation


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


class BookUrlSerializerWithCustomLink(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
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

    def to_representation(self, *args, **kwargs):
        representation = super().to_representation(*args, **kwargs)

        representation['custom_links'] = 'http://custom.com/link'

        return representation
