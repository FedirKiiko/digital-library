from django import forms
from django.contrib.auth.forms import UserCreationForm

from digital_library.models import (
    Reader,
    ReaderBook,
    Book,
    Genre,
    Author,
    Shelf
)


class ReaderRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Reader
        fields = UserCreationForm.Meta.fields + (
            "email",
            "birth_date",
            "avatar"
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "avatar": forms.FileInput(attrs={"class": "form-control-file"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"


class ReaderBookForm(forms.ModelForm):
    class Meta:
        model = ReaderBook
        fields = ["rating", "review"]
        widgets = {
            "review": forms.Textarea(attrs={"rows": 3}),
        }


class ReaderUpdateForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ["first_name", "last_name", "email", "birth_date", "avatar"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "avatar": forms.FileInput(attrs={"class": "form-control-file"}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "pages",
            "year_published",
            "publisher",
            "cover_image",
            "genres",
            "authors"
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "pages": forms.NumberInput(attrs={"class": "form-control"}),
            "year_published": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "publisher": forms.TextInput(attrs={"class": "form-control"}),
            "cover_image": forms.FileInput(
                attrs={"class": "form-control-file"}
            ),
            "genres": forms.CheckboxSelectMultiple,
            "authors": forms.CheckboxSelectMultiple,
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name", "description"]


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            "first_name",
            "last_name",
            "pseudonym",
            "birth_date",
            "death_date",
            "bio",
            "photo",
            "country"
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "pseudonym": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "death_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "photo": forms.FileInput(attrs={"class": "form-control-file"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }


class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ["name"]

    def __init__(self, *args, reader: Reader | None = None, **kwargs) -> None:
        self.reader = reader
        super().__init__(*args, **kwargs)

    def clean_name(self) -> str:
        name = self.cleaned_data["name"]
        if Shelf.objects.filter(reader=self.reader, name=name).exists():
            raise forms.ValidationError(
                "You already have a shelf with this name."
            )
        return name


class BookSearchForm(forms.Form):
    search = forms.CharField(max_length=255, required=False)


class GenreSearchForm(forms.Form):
    search = forms.CharField(max_length=255, required=False)


class AuthorSearchForm(forms.Form):
    search = forms.CharField(max_length=255, required=False)
