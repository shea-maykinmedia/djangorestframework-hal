import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..app.models import Author, Book


class BookTests(APITestCase):

    def test_book_retrieve(self):
        """
        test /books/{id} GET:
        """

        author = Author.objects.create(name='Tolstoy')
        book = Book.objects.create(author=author, pages=1000, title='War and peace')
        book_url = reverse('book-detail', args=[book.uuid])

        response = self.client.get(book_url, HTTP_HOST='localhost')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        author_url = reverse('author-detail', kwargs={'uuid': author.uuid})

        self.assertEqual(
            data,
            {
                '_links': {
                    'author': {'href': f'http://localhost{author_url}'},
                    'self': {'href': f'http://localhost{book_url}'}
                },
                'title': 'War and peace',
                'pages': 1000
            }
        )

    def test_book_list(self):
        """
        test /books GET:
        """

        author = Author.objects.create(name='Tolstoy')
        book = Book.objects.create(author=author, pages=1000, title='War and peace')

        book_list_url = reverse('book-list')

        response = self.client.get(book_list_url, HTTP_HOST='localhost')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        book_url = reverse('book-detail', args=[book.uuid])
        author_url = reverse('author-detail', kwargs={'uuid': author.uuid})

        self.assertEqual(
            data,
            {
                '_links': {
                    'self': {'href': f'http://localhost{book_list_url}'}
                },
                '_embedded': {
                    'book': [
                        {
                            '_links': {
                                'author': {'href': f'http://localhost{author_url}'},
                                'self': {'href': f'http://localhost{book_url}'}
                            },
                            'title': 'War and peace',
                            'pages': 1000
                        }
                    ]
                }
            }

        )

    def test_book_create(self):
        """
        test /books POST:
        """
        author = Author.objects.create(name='Tolstoy')
        author_url = reverse('author-detail', kwargs={'uuid': author.uuid})
        book_url = reverse('book-list')
        request_data = {
            '_links': {'author': {'href': f'http://localhost{author_url}'}},
            'title': 'War and peace',
            'pages': 1000
        }

        # client = RequestsClient()
        response = self.client.post(
            book_url,
            json.dumps(request_data),
            HTTP_HOST='localhost',
            # format='json',
            content_type='application/hal+json',
            headers={'Content-Type': 'application/hal+json'}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

        book = Book.objects.get()

        self.assertEqual(book.title, 'War and peace')
        self.assertEqual(book.author, author)

    def test_author_list_pagination(self):
        """
        test /authors GET: with pagination
        """
        author1 = Author.objects.create(name='Tolstoy', email='leo@tolstoy.ru')
        author2 = Author.objects.create(name='Vonnegut', email='kurt@vonnegut.com')

        author_list_url = reverse('author-list')

        response = self.client.get(author_list_url, HTTP_HOST='localhost')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        author1_url = reverse('author-detail', kwargs={'uuid': author1.uuid})

        self.assertEqual(
            data,
            {
                '_links': {
                    'next': {'href': f'http://localhost{author_list_url}?page=2'},
                    'previous': {'href': None},
                    'self': {'href': f'http://localhost{author_list_url}'}
                },
                '_embedded': {
                    'author': [
                        {
                            '_links': {
                                'self': {'href': f'http://localhost{author1_url}'}
                            },
                            'name': 'Tolstoy',
                            'email': 'leo@tolstoy.ru'}
                    ]
                },
                'count': 2
            }
        )
