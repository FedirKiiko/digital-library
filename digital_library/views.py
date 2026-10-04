import random
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, F, Q
from django.db.models.aggregates import Avg
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from digital_library.forms import (
    ReaderRegisterForm,
    ReaderBookForm,
    BookForm,
    GenreForm,
    AuthorForm,
    ShelfForm,
    BookSearchForm, GenreSearchForm, AuthorSearchForm
)
from digital_library.mixins import StaffRequiredMixin
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

    def get_queryset(self) -> QuerySet:
        queryset = Book.objects.annotate(
                avg_rating=Avg("reader_books__rating"),
                avg_rating_percent=(F("avg_rating") / 10 * 100)
            ).prefetch_related("authors", "genres")
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(title__icontains=search_query).distinct()
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = BookSearchForm(
            initial={"search": self.request.GET.get("search", "")}
        )
        return context


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
        context["avg_rating_percent"] = (context["avg_rating"] / 10 * 100) if context["avg_rating"] else 0
        context["ratings_count"] = book.reader_books.filter(rating__isnull=False).count()
        context["reviews_count"] = book.reader_books.exclude(review__isnull=True).exclude(review__exact="").count()

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

        if request.POST.get("form_type") == "shelves":
            selected_ids = request.POST.getlist("shelves")
            update_reader_shelves(user=request.user, book=book, selected_ids=selected_ids)
        elif request.POST.get("form_type") == "rating":
            reader_book = get_or_create_reader_book(user=request.user, book=book)
            form = ReaderBookForm(request.POST, instance=reader_book)
            if form.is_valid():
                form.save()

        return redirect("digital_library:book-detail", pk=book.pk)


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    template_name = "digital_library/book_form.html"
    form_class = BookForm
    success_url = reverse_lazy("digital_library:book-list")


class BookUpdateView(StaffRequiredMixin, generic.UpdateView):
    model = Book
    template_name = "digital_library/book_form.html"
    form_class = BookForm
    success_url = reverse_lazy("digital_library:book-list")


class BookDeleteView(StaffRequiredMixin, generic.DeleteView):
    model = Book
    success_url = reverse_lazy("digital_library:book-list")
    template_name = "digital_library/book_confirm_delete.html"


class GenreListView(generic.ListView):
    template_name = "digital_library/genre_list.html"
    model = Genre
    paginate_by = 20

    def get_queryset(self) -> QuerySet:
        queryset = Genre.objects.prefetch_related("books")
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = GenreSearchForm(
            initial={"search": self.request.GET.get("search", "")}
        )
        return context


class GenreDetailView(generic.DetailView):
    template_name = "digital_library/genre_detail.html"
    model = Genre
    queryset = Genre.objects.prefetch_related("books")


class GenreCreateView(StaffRequiredMixin, generic.CreateView):
    model = Genre
    template_name = "digital_library/genre_form.html"
    form_class = GenreForm
    success_url = reverse_lazy("digital_library:genre-list")


class GenreUpdateView(StaffRequiredMixin, generic.UpdateView):
    model = Genre
    template_name = "digital_library/genre_form.html"
    form_class = GenreForm
    success_url = reverse_lazy("digital_library:genre-list")


class GenreDeleteView(StaffRequiredMixin, generic.DeleteView):
    model = Genre
    success_url = reverse_lazy("digital_library:genre-list")
    template_name = "digital_library/genre_confirm_delete.html"


class AuthorsListView(generic.ListView):
    template_name = "digital_library/author_list.html"
    model = Author
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        queryset = Author.objects.prefetch_related("books")
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(pseudonym__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = AuthorSearchForm(
            initial={"search": self.request.GET.get("search", "")}
        )
        return context


class AuthorsDetailView(generic.DetailView):
    template_name = "digital_library/author_detail.html"
    model = Author
    queryset = Author.objects.prefetch_related("books")


class AuthorsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Author
    template_name = "digital_library/author_form.html"
    form_class = AuthorForm
    success_url = reverse_lazy("digital_library:author-list")


class AuthorsUpdateView(StaffRequiredMixin, generic.UpdateView):
    model = Author
    template_name = "digital_library/author_form.html"
    form_class = AuthorForm
    success_url = reverse_lazy("digital_library:author-list")


class AuthorsDeleteView(StaffRequiredMixin, generic.DeleteView):
    model = Author
    success_url = reverse_lazy("digital_library:author-list")
    template_name = "digital_library/author_confirm_delete.html"



class MyLibraryView(LoginRequiredMixin, generic.ListView):
    model = Shelf
    template_name = "digital_library/my_library.html"
    context_object_name = "shelves"

    def get_queryset(self) -> QuerySet:
        return Shelf.objects.filter(
            reader=self.request.user
        ).prefetch_related("books")


class ShelfCreateView(LoginRequiredMixin, generic.CreateView):
    model = Shelf
    form_class = ShelfForm
    template_name = "digital_library/shelf_form.html"
    success_url = reverse_lazy("digital_library:my-library")

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["reader"] = self.request.user
        return kwargs

    def form_valid(self, form: ShelfForm) -> HttpResponse:
        form.instance.reader = self.request.user
        return super().form_valid(form)
