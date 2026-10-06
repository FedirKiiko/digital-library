from django.contrib.auth import get_user_model
from django.test import TestCase

from digital_library.models import Book, Shelf, ReaderBook
from digital_library.services import get_or_create_reader_book, update_reader_shelves

Reader = get_user_model()


class GetOrCreateReaderBookTests(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create_user(
            username="reader1", password="testpass123"
        )
        self.book = Book.objects.create(
            title="Dune", pages=412, year_published=1965
        )

    def test_creates_reader_book_if_not_exists(self):
        self.assertEqual(ReaderBook.objects.count(), 0)
        reader_book = get_or_create_reader_book(user=self.reader, book=self.book)
        self.assertEqual(ReaderBook.objects.count(), 1)
        self.assertEqual(reader_book.reader, self.reader)
        self.assertEqual(reader_book.book, self.book)

    def test_returns_existing_reader_book_without_duplicating(self):
        existing = ReaderBook.objects.create(
            reader=self.reader, book=self.book, rating=7
        )
        result = get_or_create_reader_book(user=self.reader, book=self.book)
        self.assertEqual(ReaderBook.objects.count(), 1)
        self.assertEqual(result.pk, existing.pk)
        self.assertEqual(result.rating, 7)


class UpdateReaderShelvesTests(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create_user(
            username="reader1", password="testpass123"
        )
        self.book = Book.objects.create(
            title="Dune", pages=412, year_published=1965
        )
        self.shelf_a = Shelf.objects.get(reader=self.reader, name="Want to read")
        self.shelf_b = Shelf.objects.get(reader=self.reader, name="Read")

    def test_adds_book_to_selected_shelves(self):
        update_reader_shelves(
            user=self.reader,
            book=self.book,
            selected_ids=[str(self.shelf_a.id)],
        )
        self.assertIn(self.book, self.shelf_a.books.all())
        self.assertNotIn(self.book, self.shelf_b.books.all())

    def test_removes_book_from_deselected_shelves(self):
        self.shelf_a.books.add(self.book)
        update_reader_shelves(user=self.reader, book=self.book, selected_ids=[])
        self.assertNotIn(self.book, self.shelf_a.books.all())

    def test_does_not_affect_other_readers_shelves(self):
        other_reader = Reader.objects.create_user(
            username="reader2", password="testpass123"
        )
        other_shelf = Shelf.objects.get(reader=other_reader, name="Want to read")
        update_reader_shelves(
            user=self.reader,
            book=self.book,
            selected_ids=[str(self.shelf_a.id)],
        )
        self.assertNotIn(self.book, other_shelf.books.all())
