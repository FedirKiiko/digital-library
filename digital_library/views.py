import random
from typing import Any

from django.db.models.aggregates import Avg
from django.views import generic

from digital_library.models import Book, Genre, Author


class IndexView(generic.TemplateView):
    template_name = "digital_library/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        top_books = list(
            Book.objects.annotate(avg_rating=Avg("reader_books__rating"))
            .filter(avg_rating__isnull=False)
            .order_by("-avg_rating")[:20]
        )
        context["books"] = random.sample(top_books, min(10, len(top_books)))
        return context


class BookListView(generic.ListView):
    template_name = "digital_library/book_list.html"
    model = Book
    paginate_by = 10
    queryset = Book.objects.prefetch_related("authors", "genres")


class BookDetailView(generic.DetailView):
    model = Book


class GenreListView(generic.ListView):
    template_name = "digital_library/genre_list.html"
    model = Genre
    paginate_by = 20
    queryset = Genre.objects.prefetch_related("books")


class GenreDetailView(generic.DetailView):
    template_name = "digital_library/genre_detail.html"
    model = Genre
    queryset = Genre.objects.prefetch_related("books")


class AuthorsListView(generic.ListView):
    template_name = "digital_library/author_list.html"
    model = Author
    paginate_by = 10
    queryset = Author.objects.prefetch_related("books")


class AuthorsDetailView(generic.DetailView):
    template_name = "digital_library/author_detail.html"
    model = Author
    queryset = Author.objects.prefetch_related("books")
