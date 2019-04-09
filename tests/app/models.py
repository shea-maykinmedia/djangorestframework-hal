import uuid as _uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    uuid = models.UUIDField(
        unique=True, default=_uuid.uuid4,
        help_text=_('Unique resource identifier (UUID4)')
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)

    def __str__(self):
        return f'Author: {self.name}'


class Book(models.Model):
    uuid = models.UUIDField(
        unique=True, default=_uuid.uuid4,
        help_text=_('Unique resource identifier (UUID4)')
    )
    title = models.CharField(max_length=1000)
    pages = models.IntegerField(null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'Book: {self.title}'
