import json
from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.forms import ValidationError

from .models import Property


class HasPropertiesMixin:
    """
    Mixin for models that can have properties attached to them.
    """

    def get_property(self, key, default=None):  # pragma: no coverage
        """
        Get a property value by key
        """
        try:
            ct = ContentType.objects.get_for_model(self)
            prop = Property.objects.get(content_type=ct, object_id=self.id, key=key)
            return prop.get_typed_value()
        except Property.DoesNotExist:
            return default

    def set_property(
        self, key, value, description=None, type_name="str"
    ):  # pragma: no coverage
        """
        Set a property value by key with optional type specification
        """
        if type_name not in dict(Property.PropertyType.choices):
            raise ValueError(f"Invalid property type: {type_name}")

        ct = ContentType.objects.get_for_model(self)
        try:
            prop = Property.objects.get(content_type=ct, object_id=self.id, key=key)
            prop.type = type_name
        except Property.DoesNotExist:
            prop = Property(
                content_type=ct,
                object_id=self.id,
                key=key,
                type=type_name,
                description=description,
            )

        try:
            if type_name == "int":
                int(value)
            elif type_name == "float":
                float(value)
            elif type_name == "datetime":
                if not isinstance(value, datetime):
                    datetime.fromisoformat(str(value))
            elif type_name == "json":
                if not isinstance(value, str):
                    json.dumps(value)
                else:
                    json.loads(value)
        except (ValueError, TypeError, json.JSONDecodeError):
            raise ValidationError(f"Invalid value for type {type_name}")

        prop.set_typed_value(value)
        if prop.description != description:
            prop.description = description
        prop.save()
        return prop

    def delete_property(self, key):  # pragma: no coverage
        """
        Delete a property by key
        """
        ct = ContentType.objects.get_for_model(self)
        return Property.objects.filter(
            content_type=ct, object_id=self.id, key=key
        ).delete()

    def get_all_properties(self):  # pragma: no coverage
        """
        Get all properties for this object
        """
        ct = ContentType.objects.get_for_model(self)
        return Property.objects.filter(content_type=ct, object_id=self.id)
