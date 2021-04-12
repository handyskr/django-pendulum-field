from django.forms import ModelForm
from .models import *

__all__ = ["SomethingForm"]


class SomethingForm(ModelForm):
    class Meta:
        model = Something
        fields = ["id", "some_dt"]
