from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.etags.widgets import TagsInputWidget

# from apps.repo.models.project import Project
from ..models import Document, Folder, Version


class AddFolderForm(forms.ModelForm):
    """
    Form to add a folder
    """

    class Meta:
        model = Folder

        exclude = (
            "owner",
            "parent",
        )


class UpdateElementForm(forms.ModelForm):
    """
    Form to update elements (folder, document)
    """

    tags = forms.CharField(
        widget=TagsInputWidget(attrs={"placeholder": "Enter comma-separated tags"}),
        required=False,
    )

    class Meta:
        model = Folder

        exclude = (
            "owner",
            "parent",
        )

    def clean_tags(self):  # pragma: no coverage
        """This is called when the form is submitted."""
        tags_input = self.cleaned_data.get("tags", "")

        # Remove the '#' from each tag before saving to the database
        clean_tags = [
            tag.strip().lstrip("#") for tag in tags_input.split(",") if tag.strip()
        ]

        # Check if there are more than 5 tags
        if len(clean_tags) > settings.MAX_TAG_COUNT:
            raise ValidationError(
                f"Too many tags. Enter {settings.MAX_TAG_COUNT} or fewer and try again."
            )

        return ", ".join(clean_tags)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document

        exclude = (
            "owner",
            "parent",
        )


class AddDocumentForm(DocumentForm):
    """
    Form to add a document
    """

    pass


class UpdateDocumentForm(DocumentForm):
    """
    Form to add a document
    """

    pass


class AddVersionForm(forms.ModelForm):
    """
    Form to add version (in this case actual text content to create a file) for a document
    """

    content = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Version

        exclude = (
            "parent",
            "tag",
        )


class UpdateDocumentContentForm(forms.ModelForm):
    """
    Form to add version (in this case actual text content to create a file) for a document
    """

    content = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Version

        exclude = (
            "parent",
            "tag",
        )


class UpdateVersionForm(forms.ModelForm):
    """
    Form to update a version (content file) for a document
    """

    CHOICES = [
        ("Major", "Major"),  # major version
        ("Minor", "Minor"),  # minor version
    ]

    change_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
    )

    class Meta:
        model = Version
        exclude = ("parent", "tag")
