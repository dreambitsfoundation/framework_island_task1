import json
from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from management_app.validators import validate_phone_number
from management_app.models import Supplier, Inventory

TEST_CONTENT_DIRECTORY = "management_app/tests/test_elements"


class TestSupplierModel(TestCase):
    """This is the test suite for Supplier"""

    def setUp(self) -> None:
        happy_payload = open(f"{TEST_CONTENT_DIRECTORY}/supplier_happy.json")
        self.happy_payload = json.load(happy_payload)
        unhappy_payload = open(f"{TEST_CONTENT_DIRECTORY}/supplier_unhappy.json")
        self.unhappy_payload = json.load(unhappy_payload)

    def test_all_records_are_successfully_created(self):
        suppliers = []
        for supplier_data in self.happy_payload:
            supplier = Supplier(**supplier_data)
            supplier.save()
            suppliers.append(supplier)

        for index, instance in enumerate(suppliers):
            self.assertEqual(instance.name, self.happy_payload[index]["name"])

    def test_malformed_supplier_payload(self):
        """
        This test should fail because the payload only contains value for name
        and other fields are not assigned any value. This is expected to throw
        django.core.exeption.IntegrityError due to failure in Not NULL contraint.
        """
        supplier = Supplier(**self.unhappy_payload)
        self.assertRaises(IntegrityError, supplier.save)

    def test_phone_number_validator(self):
        self.assertRaises(ValidationError, validate_phone_number, 123)
        self.assertEqual(validate_phone_number(1234567890), None)


class TestInventoryModel(TestCase):
    """This is the test suite for Inventory"""

    def setUp(self) -> None:
        happy_payload = open(f"{TEST_CONTENT_DIRECTORY}/supplier_happy.json")
        happy_path_payload = json.load(happy_payload)
        self.supplier = Supplier(**happy_path_payload[0])
        self.supplier.save()

    def test_create_new_inventory(self):
        json_file = open(f"{TEST_CONTENT_DIRECTORY}/inventory_happy.json")
        payload = json.load(json_file)
        payload["image"] = f"{TEST_CONTENT_DIRECTORY}/inventory_image/toy_image.webp"
        payload["supplier"] = self.supplier

        inventory = Inventory.objects.create(**payload)
        inventory.save()

        self.assertEqual(inventory.name, payload["name"])
        self.assertEqual(inventory.image, payload["image"])

    def test_malformed_inventory_payload(self):
        """
        In this test we're not supplying the supplier_id into the payload,
        which is expected to raise IntegrityError, since the supplier_id
        field has NOT NULL constraint.
        """
        json_file = open(f"{TEST_CONTENT_DIRECTORY}/inventory_happy.json")
        payload = json.load(json_file)
        payload["image"] = f"{TEST_CONTENT_DIRECTORY}/inventory_image/toy_image.webp"

        inventory = Inventory(**payload)

        self.assertRaises(IntegrityError, inventory.save)
