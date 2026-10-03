from django import forms
from django.contrib.auth.forms import UserCreationForm

from digital_library.models import Reader, ReaderBook


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
