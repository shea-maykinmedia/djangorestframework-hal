from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .viewsets import AuthorViewSet, BookViewSet, AuthorHalViewSet, BookHalViewSet


router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'authors_hal', AuthorHalViewSet)
router.register(r'books_hal', BookHalViewSet)

urlpatterns = [
        # actual API
        path('', include(router.urls)),
]
