from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.repo.models import Folder
from apps.repo.tests.utils import (
    TEST_USER,
    get_test_document,
    get_test_folder,
    get_test_user,
)

from .models import Property


class AddElementPropertiesViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_folder = get_test_folder(parent=self.test_user.profile.home_folder)
        self.test_document = get_test_document(
            parent=self.test_user.profile.home_folder
        )

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.get(
            reverse(
                "repo:properties:add_properties",
                args=[self.test_folder.type, self.test_folder.pk],
            )
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse(
                "repo:properties:add_properties",
                args=[self.test_document.type, self.test_document.pk],
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:properties:add_properties",
                args=[self.test_folder.type, self.test_folder.pk],
            ),
            data={
                "key[]": "test_key",
                "value[]": "true",
                "type[]": "bool",
                "description[]": "a test bool",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Property.objects.get(key="test_key"))


class UpdateElementPropertyViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_folder = get_test_folder(parent=self.test_user.profile.home_folder)

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        property = self.test_folder.set_property(
            key="test_key", value="test value", description="test description"
        )

        response = self.client.get(
            reverse("repo:properties:update_property", args=[property.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        property = self.test_folder.set_property(
            key="test_key", value="test value", description="test description"
        )

        response = self.client.post(
            reverse("repo:properties:update_property", args=[property.pk]),
            data={
                "key": "test_key",
                "value": "some new value",
                "description": "test description 2",
                "type": "str",
            },
        )
        self.assertEqual(response.status_code, 302)

        # Missing required field test
        response = self.client.post(
            reverse("repo:properties:update_property", args=[property.pk]),
            data={
                "key": "test_key",
                "value": "some new value",
                "description": "test description 2",
            },
        )
        self.assertEqual(response.status_code, 200)


class PropertyModelTest(TestCase):
    def setUp(self):
        """Create a test folder for all tests to use"""
        self.test_user = get_test_user()
        self.home_folder = self.test_user.profile.home_folder
        self.folder = get_test_folder(parent=self.home_folder)

    def test_string_properties(self):
        """Test setting and getting string properties"""
        # Set a string property
        self.folder.set_property("description", "Test folder for properties")

        # Verify the property
        self.assertEqual(
            self.folder.get_property("description"), "Test folder for properties"
        )

        # Update the property
        self.folder.set_property("description", "Updated description")
        self.assertEqual(self.folder.get_property("description"), "Updated description")

    def test_boolean_properties(self):
        """Test setting and getting boolean properties"""
        # Test True value
        self.folder.set_property("is_archived", True, type_name="bool")
        self.assertTrue(self.folder.get_property("is_archived"))

        # Test False value
        self.folder.set_property("is_readonly", False, type_name="bool")
        self.assertFalse(self.folder.get_property("is_readonly"))

    def test_numeric_properties(self):
        """Test setting and getting numeric properties"""
        # Test integer
        self.folder.set_property("max_size_mb", 500, type_name="int")
        self.assertEqual(self.folder.get_property("max_size_mb"), 500)
        self.assertIsInstance(self.folder.get_property("max_size_mb"), int)

        # Test float
        self.folder.set_property("priority", 2.5, type_name="float")
        self.assertEqual(self.folder.get_property("priority"), 2.5)
        self.assertIsInstance(self.folder.get_property("priority"), float)

    def test_datetime_properties(self):
        """Test setting and getting datetime properties"""
        test_date = datetime.now().replace(
            microsecond=0
        )  # Remove microseconds for comparison
        self.folder.set_property("next_review", test_date, type_name="datetime")

        stored_date = self.folder.get_property("next_review").replace(microsecond=0)
        self.assertEqual(stored_date, test_date)

    def test_json_properties(self):
        """Test setting and getting JSON properties"""
        # Test list
        test_list = ["pdf", "doc", "txt"]
        self.folder.set_property("allowed_extensions", test_list, type_name="json")
        self.assertEqual(self.folder.get_property("allowed_extensions"), test_list)

        # Test dictionary
        test_dict = {
            "created_by": "admin",
            "department": "engineering",
            "tags": ["important", "confidential"],
        }
        self.folder.set_property("metadata", test_dict, type_name="json")
        self.assertEqual(self.folder.get_property("metadata"), test_dict)

    def test_property_deletion(self):
        """Test property deletion"""
        # Create a property
        self.folder.set_property("test_key", "test_value")
        self.assertEqual(self.folder.get_property("test_key"), "test_value")

        # Delete the property
        self.folder.delete_property("test_key")
        self.assertIsNone(self.folder.get_property("test_key"))

    def test_get_all_properties(self):
        """Test retrieving all properties for an object"""
        # Create multiple properties
        test_props = {
            "str_prop": ("string value", "str"),
            "int_prop": (42, "int"),
            "bool_prop": (True, "bool"),
        }

        for key, (value, type_name) in test_props.items():
            self.folder.set_property(key, value, type_name=type_name)

        # Get all properties
        all_props = self.folder.get_all_properties()
        self.assertEqual(all_props.count(), len(test_props))

        # Verify each property
        for prop in all_props:
            self.assertTrue(prop.key in test_props)
            original_value = test_props[prop.key][0]
            self.assertEqual(prop.get_typed_value(), original_value)

    def test_property_querying(self):
        """Test querying objects by their properties"""
        # Create a property to query by
        self.folder.set_property("department", "engineering", type_name="str")

        # Query folders with this property
        folders = Folder.objects.filter(
            properties__key="department", properties__value="engineering"
        )

        self.assertEqual(folders.count(), 1)
        self.assertEqual(folders.first(), self.folder)

    def test_default_values(self):
        """Test default value handling for non-existent properties"""
        default_value = "default"
        value = self.folder.get_property("nonexistent", default=default_value)
        self.assertEqual(value, default_value)

    def test_invalid_type(self):
        """Test handling of invalid property types"""
        with self.assertRaises(ValueError):
            self.folder.set_property("test", "value", type_name="invalid_type")

    def test_invalid_value_for_type(self):
        """Test handling of invalid values for types"""
        # Test invalid integer
        with self.assertRaises(ValidationError):
            self.folder.set_property("test_number", "not a number", type_name="int")

        # Test invalid float
        with self.assertRaises(ValidationError):
            self.folder.set_property("test_float", "not a float", type_name="float")

        # Test invalid datetime
        with self.assertRaises(ValidationError):
            self.folder.set_property("test_date", "not a date", type_name="datetime")

        # Test invalid JSON
        with self.assertRaises(ValidationError):
            self.folder.set_property("test_json", "{invalid json}", type_name="json")

    def test_unique_properties(self):
        """Test that properties are unique per object and key"""
        # Set initial property
        self.folder.set_property("unique_test", "initial value")

        # Update same property
        self.folder.set_property("unique_test", "updated value")

        # Verify only one property exists with the updated value
        props = Property.objects.filter(
            content_type=ContentType.objects.get_for_model(self.folder),
            object_id=self.folder.id,
            key="unique_test",
        )
        self.assertEqual(props.count(), 1)
        self.assertEqual(props.first().value, "updated value")

    def test_property_type_persistence(self):
        """Test that property types persist through updates"""
        # Set initial numeric property
        self.folder.set_property("number", 42, type_name="int")

        # Update value but keep type
        self.folder.set_property("number", 43, type_name="int")

        # Verify type remained 'int'
        prop = Property.objects.get(
            content_type=ContentType.objects.get_for_model(self.folder),
            object_id=self.folder.id,
            key="number",
        )
        self.assertEqual(prop.type, Property.PropertyType.INTEGER)
        self.assertIsInstance(prop.get_typed_value(), int)

    def test_null_value_handling(self):
        """Test handling of null/None values"""
        self.folder.set_property("nullable", None)
        self.assertIsNone(self.folder.get_property("nullable"))

        # Update None to value
        self.folder.set_property("nullable", "not null anymore")
        self.assertEqual(self.folder.get_property("nullable"), "not null anymore")

        # Update back to None
        self.folder.set_property("nullable", None)
        self.assertIsNone(self.folder.get_property("nullable"))
