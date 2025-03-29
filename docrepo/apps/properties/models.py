import json
from datetime import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models


class Property(models.Model):
    """
    A generic property model that can be attached to any model instance
    through content type framework. Includes type validation for values.
    """

    class PropertyType(models.TextChoices):
        STRING = "str", "String"
        INTEGER = "int", "Integer"
        FLOAT = "float", "Float"
        BOOLEAN = "bool", "Boolean"
        DATETIME = "datetime", "DateTime"
        JSON = "json", "JSON"

    # The model instance this property belongs to
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

    # The key, value, and type fields
    key = models.CharField(max_length=255, db_index=True)
    value = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.STRING,
        db_index=True,
    )

    # When the property was created and last modified
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        unique_together = ("content_type", "object_id", "key")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["key"]),
            models.Index(fields=["created"]),
        ]

    def clean(self):  # pragma: no coverage
        """
        Validate that the content_type is one of the allowed models
        and the value matches the specified type
        """
        if not self.content_type:
            raise ValidationError("Content type is required")

        # Validate allowed models
        allowed_models = ["document", "folder", "project"]
        if self.content_type.model.lower() not in allowed_models:
            raise ValidationError(
                f'Property can only be attached to the following models: {", ".join(allowed_models)}'
            )

        # Validate the type choice is valid
        if self.type not in dict(self.PropertyType.choices):
            raise ValidationError(f"Invalid property type: {self.type}")

        # Skip validation if value is None
        if self.value is None:
            return

        # Validate value type
        try:
            if self.type == self.PropertyType.INTEGER:
                int(self.value)
            elif self.type == self.PropertyType.FLOAT:
                float(self.value)
            elif self.type == self.PropertyType.JSON:
                json.loads(self.value)
            elif self.type == self.PropertyType.DATETIME:
                datetime.fromisoformat(self.value)
            elif self.type == self.PropertyType.BOOLEAN:
                if self.value.lower() not in ["true", "false", "1", "0"]:
                    raise ValueError("Boolean value must be true/false or 1/0")
        except (ValueError, json.JSONDecodeError, TypeError) as e:
            raise ValidationError(f"Invalid value for type {self.type}: {str(e)}")

    def save(self, *args, **kwargs):  # pragma: no coverage
        # Convert value to string representation
        self.clean()
        super().save(*args, **kwargs)

    def get_typed_value(self):  # pragma: no coverage
        """
        Returns the value converted to its proper Python type
        """
        if self.value is None:
            return None

        try:
            if self.type == self.PropertyType.STRING:
                return str(self.value)
            elif self.type == self.PropertyType.INTEGER:
                return int(self.value)
            elif self.type == self.PropertyType.FLOAT:
                return float(self.value)
            elif self.type == self.PropertyType.BOOLEAN:
                if isinstance(self.value, bool):
                    return self.value
                return str(self.value).lower() == "true"
            elif self.type == self.PropertyType.DATETIME:
                return datetime.fromisoformat(self.value)
            elif self.type == self.PropertyType.JSON:
                return json.loads(self.value)
        except (ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Cannot convert value to type {self.type}: {str(e)}")

        return self.value

    def set_typed_value(self, value):  # pragma: no coverage
        """
        Converts the input value to a string representation based on the property type.
        Raises ValidationError if value cannot be converted to the specified type.
        """
        if value is None:
            self.value = None
            return

        try:
            if self.type == self.PropertyType.INTEGER:
                int(value)  # Validate it can be converted to int
                self.value = str(value)
            elif self.type == self.PropertyType.FLOAT:
                float(value)  # Validate it can be converted to float
                self.value = str(value)
            elif self.type == self.PropertyType.JSON:
                # For JSON type, try to serialize it to validate
                self.value = json.dumps(value)
            elif self.type == self.PropertyType.DATETIME:
                if not isinstance(value, datetime):
                    datetime.fromisoformat(str(value))  # Validate datetime string
                self.value = (
                    value.isoformat() if isinstance(value, datetime) else str(value)
                )
            elif self.type == self.PropertyType.BOOLEAN:
                self.value = str(bool(value)).lower()
            else:  # STRING type
                self.value = str(value)
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            raise ValidationError(f"Invalid value for type {self.type}: {str(e)}")

    def __str__(self):  # pragma: no coverage
        return f"{self.content_object} - {self.key}: {self.value} ({self.type})"
