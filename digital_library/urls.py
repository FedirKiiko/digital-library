from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    IndexView,
    GenreListView,
    GenreDetailView,
    AuthorsListView,
    AuthorsDetailView, RegisterView, MyLibraryView, BookCreateView, BookUpdateView, BookDeleteView, GenreCreateView,
    GenreUpdateView, GenreDeleteView, AuthorsCreateView, AuthorsUpdateView, AuthorsDeleteView
)

app_name = "digital_library"

urlpatterns = (
    path("", IndexView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),

    path("books/", BookListView.as_view(), name="book-list"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),

    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("genres/create/", GenreCreateView.as_view(), name="genre-create"),
    path("genres/<int:pk>", GenreDetailView.as_view(), name="genre-detail"),
    path("genres/<int:pk>/update/", GenreUpdateView.as_view(), name="genre-update"),
    path("genres/<int:pk>/delete/", GenreDeleteView.as_view(), name="genre-delete"),

    path("authors/", AuthorsListView.as_view(), name="author-list"),
    path("authors/create/", AuthorsCreateView.as_view(), name="author-create"),
    path("authors/<int:pk>",AuthorsDetailView.as_view(), name="author-detail"),
    path("authors/<int:pk>/update/", AuthorsUpdateView.as_view(), name="author-update"),
    path("authors/<int:pk>/delete/", AuthorsDeleteView.as_view(), name="author-delete"),

    path("my_library/", MyLibraryView.as_view(), name="my-library"),
)