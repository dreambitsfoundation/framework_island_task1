import json
import uuid

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from management_app.models import Supplier
from management_app.forms import SupplierForm, InventoryForm

TEST_CONTENT_DIRECTORY = "management_app/tests/test_elements"


class TestSupplierForm(TestCase):
    """This is the test suite for Supplier"""

    def setUp(self) -> None:
        happy_path_request_payload = open(
            f"{TEST_CONTENT_DIRECTORY}/supplier_happy.json"
        )
        self.happy_payload = json.load(happy_path_request_payload)
        unhappy_path_request_payload = open(
            f"{TEST_CONTENT_DIRECTORY}/supplier_unhappy.json"
        )
        self.unhappy_payload = json.load(unhappy_path_request_payload)

    def test_all_records_are_successfully_created(self):
        suppliers = []
        for supplier_data in self.happy_payload:
            supplier_form = SupplierForm(supplier_data)
            self.assertTrue(supplier_form.is_valid())
            instance = supplier_form.save()
            suppliers.append(instance)

        for index, instance in enumerate(suppliers):
            self.assertEqual(instance.name, self.happy_payload[index]["name"])

    def test_malformed_supplier_payload(self):
        """
        This test should fail because the payload only contains value for name
        and other fields are not assigned any value. This is expected to throw
        ValueError becuase the data wont be validated.
        """
        supplier_form = SupplierForm(self.unhappy_payload)
        self.assertRaises(ValueError, supplier_form.save)


class TestInventory(TestCase):
    """This is the test suite for Inventory"""

    def setUp(self) -> None:
        happy_payload = open(f"{TEST_CONTENT_DIRECTORY}/supplier_happy.json")
        happy_path_payload = json.load(happy_payload)
        self.supplier = Supplier(**happy_path_payload[0])
        self.supplier.save()

    def test_create_new_inventory_form_submission(self):
        json_file = open(f"{TEST_CONTENT_DIRECTORY}/inventory_happy.json")
        payload = json.load(json_file)
        payload["supplier"] = self.supplier

        image_file_name = str(uuid.uuid4())[:8]
        files = {
            "image": SimpleUploadedFile(
                name=f"{image_file_name}.jpeg",
                content=open(
                    f"{TEST_CONTENT_DIRECTORY}/inventory_image/toy_image.jpg", "rb"
                ).read(),
                content_type="image/jpg",
            )
        }

        inventory_form = InventoryForm(data=payload, files=files)

        self.assertTrue(inventory_form.is_valid())
        # Testing if the image file is properly loaded in the memory
        self.assertEqual(inventory_form.cleaned_data["image"], files["image"])

        inventory_model_instance = inventory_form.save()

        self.assertEqual(inventory_model_instance.name, payload["name"])
        self.assertTrue(image_file_name in inventory_model_instance.image.name)
        self.assertTrue(inventory_model_instance.supplier, self.supplier)

    def test_malformed_inventory_form_payload_submission(self):
        """
        This test should fail because we have not supplied
        complete data to the form payload.
        """
        json_file = open(f"{TEST_CONTENT_DIRECTORY}/inventory_happy.json")
        payload = json.load(json_file)

        inventory_form = InventoryForm(payload)

        self.assertFalse(inventory_form.is_valid())
