from django import forms


class TagsInputWidget(forms.TextInput):
    """
    Widget for handling tags
    """

    def format_value(self, value):
        """This is called when the form renders."""
        if value is None:
            return ""

        # Check if the tags already have '#', to avoid double prepending
        tags = [
            (f"#{tag.strip()}" if not tag.strip().startswith("#") else tag.strip())
            for tag in value.split(",")
            if tag.strip()
        ]

        return ", ".join(tags)
