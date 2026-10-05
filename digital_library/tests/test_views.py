from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from digital_library.models import Book

Reader = get_user_model()


class BookListViewTests(TestCase):
    def setUp(self):
        Book.objects.create(title="1984", pages=328, year_published=1949)
        Book.objects.create(title="Brave New World", pages=311, year_published=1932)

    def test_book_list_accessible_to_anonymous_users(self):
        response = self.client.get(reverse("digital_library:book-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1984")

    def test_book_list_search_filters_by_title(self):
        response = self.client.get(
            reverse("digital_library:book-list"), {"search": "1984"}
        )
        self.assertContains(response, "1984")
        self.assertNotContains(response, "Brave New World")


class BookCreateViewAccessTests(TestCase):
    def setUp(self):
        self.url = reverse("digital_library:book-create")
        self.reader = Reader.objects.create_user(
            username="reader1", password="testpass123"
        )

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_logged_in_reader_can_access_create_book(self):
        self.client.login(username="reader1", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class BookUpdateViewAccessTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="1984", pages=328, year_published=1949
        )
        self.url = reverse("digital_library:book-update", args=[self.book.pk])
        self.reader = Reader.objects.create_user(
            username="reader1", password="testpass123"
        )
        self.staff = Reader.objects.create_user(
            username="staffuser", password="testpass123", is_staff=True
        )

    def test_regular_reader_cannot_update_book(self):
        self.client.login(username="reader1", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_staff_can_update_book(self):
        self.client.login(username="staffuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class MyLibraryViewAccessTests(TestCase):
    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(reverse("digital_library:my-library"))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_reader_can_access_my_library(self):
        Reader.objects.create_user(username="reader1", password="testpass123")
        self.client.login(username="reader1", password="testpass123")
        response = self.client.get(reverse("digital_library:my-library"))
        self.assertEqual(response.status_code, 200)


class DefaultShelvesSignalTests(TestCase):
    def test_default_shelves_created_on_reader_registration(self):
        reader = Reader.objects.create_user(
            username="newreader", password="testpass123"
        )
        self.assertEqual(reader.shelf_set.count(), 4)
