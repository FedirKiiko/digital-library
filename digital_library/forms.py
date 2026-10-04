from django import forms
from django.contrib.auth.forms import UserCreationForm

from digital_library.models import Reader, ReaderBook, Book, Genre, Author


class ReaderRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Reader
        fields = UserCreationForm.Meta.fields + ("email", "birth_date", "avatar")



class ReaderBookForm(forms.ModelForm):
    class Meta:
        model = ReaderBook
        fields = ["rating", "review"]
        widgets = {
            "review": forms.Textarea(attrs={"rows": 3}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "pages", "year_published", "publisher", "cover_image", "genres", "authors"]
        widgets ={"genres": forms.CheckboxSelectMultiple, "authors": forms.CheckboxSelectMultiple}


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name", "description"]


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["first_name", "last_name", "pseudonym", "birth_date", "death_date", "bio", "photo", "country"]

