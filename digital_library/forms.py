from django.contrib.auth.forms import UserCreationForm

from digital_library.models import Reader


class ReaderRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Reader
        fields = UserCreationForm.Meta.fields + ("email", "birth_date", "avatar")