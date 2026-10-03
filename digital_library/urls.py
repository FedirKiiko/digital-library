from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    IndexView,
    GenreListView,
    GenreDetailView,
    AuthorsListView,
    AuthorsDetailView, RegisterView
)

app_name = "digital_library"

urlpatterns = (
    path("", IndexView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("genres/<int:pk>", GenreDetailView.as_view(), name="genre-detail"),
    path("authors/", AuthorsListView.as_view(), name="author-list"),
    path("authors/<int:pk>",AuthorsDetailView.as_view(), name="author-detail")
)