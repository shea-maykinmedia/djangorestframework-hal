from rest_framework import serializers

from .models import Author, Book


class AuthorUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('url', 'name', 'email')
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }


class BookUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('url', 'title', 'pages', 'author')
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
            'author': {
                'lookup_field': 'uuid',
            }
        }

