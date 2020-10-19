from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Author, Book
from .serializers import AuthorUrlSerializer, BookUrlSerializer, BookUrlSerializerWithCustomLink

from djangorestframework_hal.renderers import HalJSONRenderer
from djangorestframework_hal.parsers import HalJSONParser


# standart hyperlinked viewesets  - for comparing to HAL
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorUrlSerializer
    lookup_field = 'uuid'


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookUrlSerializer
    lookup_field = 'uuid'


# HAL viewsets
# with pagination
class AuthorHalViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorUrlSerializer
    renderer_classes = (HalJSONRenderer,)
    parser_classes = (HalJSONParser,)
    pagination_class = PageNumberPagination
    lookup_field = 'uuid'


# without pagination
class BookHalViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookUrlSerializer
    renderer_classes = (HalJSONRenderer,)
    parser_classes = (HalJSONParser,)
    pagination_class = None
    lookup_field = 'uuid'


class BookHalViewSetWithCustomLinkSerializer(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookUrlSerializerWithCustomLink
    renderer_classes = (HalJSONRenderer,)
    parser_classes = (HalJSONParser,)
    pagination_class = None
    lookup_field = 'uuid'
