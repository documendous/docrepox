from django import forms
from django.contrib.auth import get_user_model
from apps.projects.models import Project
from apps.repo.forms.element import UpdateElementForm


User = get_user_model()


class UpdateProjectForm(UpdateElementForm):
    """
    Form to update a project (subclasses UpdateElementForm)
    """

    class Meta:
        model = Project
        exclude = (
            "owner",
            "parent",
        )


class AddProjectForm(forms.ModelForm):
    """
    Form to add/create a new project
    """

    class Meta:
        model = Project
        exclude = [
            "folder",
            "owner",
            "is_active",
        ]


class MultipleUserSelectForm(forms.Form):
    """
    Form used for selecting multiple users
    """

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        label="Select Users",
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, **kwargs)
        if group:
            self.fields["users"].queryset = User.objects.exclude(groups=group)
