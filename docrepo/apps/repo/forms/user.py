from django import forms
from django.contrib.auth import get_user_model

from ..models import Profile

User = get_user_model()


class DateInput(forms.DateInput):
    input_type = "date"


class EmailInput(forms.EmailInput):
    input_type = "email"


class UpdateProfileForm(forms.ModelForm):
    """
    Form to update user profiles
    """

    class Meta:
        model = Profile
        fields = [
            "bio",
            "location",
            "birth_date",
        ]
        widgets = {
            "birth_date": DateInput,
        }


class UpdateUserForm(forms.ModelForm):
    """
    Form to update user account info
    """

    class Meta:
        model = User
        fields = [
            "email",
        ]
        widgets = {
            "email": EmailInput,
        }
