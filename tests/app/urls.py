from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .viewsets import (
    AuthorHalViewSet, AuthorViewSet, BookHalViewSet, BookViewSet,
    AuthorHalViewSetWithCustomLinkSerializer, BookHalViewSetWithCustomLinkSerializer
)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'authors_hal', AuthorHalViewSet)
router.register(r'authors_hal_custom', AuthorHalViewSetWithCustomLinkSerializer, basename='author-book')
router.register(r'books_hal', BookHalViewSet)
router.register(r'books_hal_custom', BookHalViewSetWithCustomLinkSerializer, basename='custom-book')

urlpatterns = [
        # actual API
        path('', include(router.urls)),
]
