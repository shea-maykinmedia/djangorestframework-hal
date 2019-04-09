from rest_framework import viewsets

from .models import Author, Book
from .serializers import AuthorUrlSerializer, BookUrlSerializer

# FIXME before
from djangorestframework_hal.renderers import HalJSONRenderer
from djangorestframework_hal.parsers import HalJSONParser


# standart hyperlinked viewesets
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorUrlSerializer
    lookup_field = 'uuid'


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookUrlSerializer
    lookup_field = 'uuid'


# drf-json-hal viewsets
class AuthorHalViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorUrlSerializer
    renderer_classes = (HalJSONRenderer,)
    parser_classes = (HalJSONParser,)
    lookup_field = 'uuid'


class BookHalViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookUrlSerializer
    renderer_classes = (HalJSONRenderer,)
    parser_classes = (HalJSONParser,)
    lookup_field = 'uuid'

