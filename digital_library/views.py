import random
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.db.models.aggregates import Avg
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic


from digital_library.forms import ReaderRegisterForm, ReaderBookForm
from digital_library.models import Book, Genre, Author, Shelf, ReaderBook
from digital_library.services import get_or_create_reader_book, update_reader_shelves


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


class RegisterView(generic.CreateView):
    form_class = ReaderRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class BookListView(generic.ListView):
    template_name = "digital_library/book_list.html"
    model = Book
    paginate_by = 10
    queryset = Book.objects.prefetch_related("authors", "genres")


class BookDetailView(generic.DetailView):
    template_name = "digital_library/book_detail.html"
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object

        context["avg_rating"] = book.reader_books.aggregate(Avg("rating"))["rating__avg"]
        context["recent_reviews"] = book.reader_books.exclude(
            review__isnull=True
        ).exclude(review__exact="").order_by("-id")[:5]

        if self.request.user.is_authenticated:
            shelves = Shelf.objects.filter(reader=self.request.user)
            context["shelves"] = shelves
            context["selected_shelf_ids"] = set(
                shelves.filter(books=book).values_list("id", flat=True)
            )
            reader_book = ReaderBook.objects.filter(
                reader=self.request.user, book=book
            ).first()
            context["form"] = ReaderBookForm(instance=reader_book)
            context["reader_book"] = reader_book
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        self.object = self.get_object()
        book = self.object

        selected_ids = request.POST.getlist("shelves")
        update_reader_shelves(user=request.user, book=book, selected_ids=selected_ids)

        reader_book = get_or_create_reader_book(user=request.user, book=book)
        form = ReaderBookForm(request.POST, instance=reader_book)
        if form.is_valid():
            form.save()

        return redirect("digital_library:book-detail", pk=book.pk)


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


class MyLibraryView(LoginRequiredMixin, generic.ListView):
    model = Shelf
    template_name = "digital_library/my_library.html"
    context_object_name = "shelves"

    def get_queryset(self) -> QuerySet:
        return Shelf.objects.filter(
            reader=self.request.user
        ).prefetch_related("books")
