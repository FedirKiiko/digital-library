import random
from typing import Any

from django.db.models.aggregates import Avg
from django.views import generic

from digital_library.models import Book


class IndexView(generic.TemplateView):
    template_name = "digital_library/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        top_books = list(
            Book.objects.annotate(avg_rating=Avg("reader_books__rating"))
            .filter(avg_rating__isnull=False)
            .order_by("-avg_rating")[:20]
        )
        context["books"] = random.sample(top_books, min(8, len(top_books)))
        return context


class BookListView(generic.ListView):
    template_name = "digital_library/book_list.html"
    model = Book
    paginate_by = 10
    queryset = Book.objects.prefetch_related("authors", "genres")


class BookDetailView(generic.DetailView):
    model = Book


class GenreListView(generic.ListView):
    pass


class GenreDetailView(generic.DetailView):
    pass


class AuthorsListView(generic.ListView):
    pass


class AuthorsDetailView(generic.DetailView):
    pass
