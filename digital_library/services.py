from digital_library.models import ReaderBook, Shelf


def get_or_create_reader_book(user, book):
    reader_book, _ = ReaderBook.objects.get_or_create(
        reader=user, book=book
    )
    return reader_book

def update_reader_shelves(user, book, selected_ids) -> None:
    for shelf in Shelf.objects.filter(reader=user):
        if str(shelf.id) in selected_ids:
            shelf.books.add(book)
        else:
            shelf.books.remove(book)
