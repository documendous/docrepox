from django import forms

from .models import Property


class UpdatePropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ("key", "value", "type", "description")
