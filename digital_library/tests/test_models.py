import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from digital_library.models import Book, Genre, Author, Shelf, ReaderBook

Reader = get_user_model()


class AuthorModelTests(TestCase):
    def test_is_alive_true_when_no_death_date(self):
        author = Author.objects.create(first_name="Haruki", last_name="Murakami")
        self.assertTrue(author.is_alive)

    def test_is_alive_false_when_death_date_set(self):
        author = Author.objects.create(
            first_name="George",
            last_name="Orwell",
            death_date=datetime.date(1950, 1, 21),
        )
        self.assertFalse(author.is_alive)

    def test_str_uses_pseudonym_when_present(self):
        author = Author.objects.create(
            first_name="Samuel",
            last_name="Clemens",
            pseudonym="Mark Twain",
        )
        self.assertIn("Mark Twain", str(author))

    def test_str_without_pseudonym(self):
        author = Author.objects.create(first_name="Jane", last_name="Austen")
        self.assertEqual(str(author), "Jane Austen")


class BookModelTests(TestCase):
    def test_str_returns_title(self):
        book = Book.objects.create(title="1984", pages=328, year_published=1949)
        self.assertEqual(str(book), "1984")

    def test_book_can_have_multiple_authors(self):
        book = Book.objects.create(title="Good Omens", pages=400, year_published=1990)
        author1 = Author.objects.create(first_name="Neil", last_name="Gaiman")
        author2 = Author.objects.create(first_name="Terry", last_name="Pratchett")
        book.authors.add(author1, author2)
        self.assertEqual(book.authors.count(), 2)


class ShelfModelTests(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create_user(
            username="reader1", password="testpass123"
        )

    def test_reader_cannot_have_two_shelves_with_same_name(self):
        # сигнал уже створив дефолтні полички при реєстрації,
        # тож перевіряємо дублікат саме з однією з них
        with self.assertRaises(Exception):
            Shelf.objects.create(reader=self.reader, name="Want to read")

    def test_different_readers_can_have_same_shelf_name(self):
        other_reader = Reader.objects.create_user(
            username="reader2", password="testpass123"
        )
        self.assertEqual(
            Shelf.objects.filter(name="Want to read").count(), 2
        )


class ReaderBookModelTests(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create_user(
            username="reader1", password="testpass123"
        )
        self.book = Book.objects.create(
            title="Dune", pages=412, year_published=1965
        )

    def test_reader_cannot_rate_same_book_twice(self):
        ReaderBook.objects.create(reader=self.reader, book=self.book, rating=8)
        with self.assertRaises(Exception):
            ReaderBook.objects.create(reader=self.reader, book=self.book, rating=5)
