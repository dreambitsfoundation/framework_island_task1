import json
import urllib
from bs4 import BeautifulSoup

from django.test import Client, TestCase
from django.conf import settings
from django.contrib.auth.models import User

from management_app.models import Inventory, Supplier


class TestProductView(TestCase):
    """This Test suite will test basic functionalities of views"""

    def setUp(self) -> None:
        self.client = Client()
        self.admin_username = "admin"
        self.admin_password = "pass1234"
        self.admin_user = User.objects.create_superuser(
            self.admin_username, "admin@test.com", self.admin_password
        )

        # Create Supplier
        supplier_data_file = open(
            "management_app/tests/test_elements/supplier_happy.json"
        )
        supplier_data = json.load(supplier_data_file)
        self.supplier = Supplier(**supplier_data[0])
        self.supplier.save()

        # Creating Inventory
        inventory_data_file = open(
            "management_app/tests/test_elements/inventory_happy.json"
        )
        inventory_data = json.load(inventory_data_file)
        inventory_data["supplier"] = self.supplier
        self.inventory = Inventory(**inventory_data)
        self.inventory.save()

    def test_unauthenticated_user_redirected_to_login_page(self):
        """
        This case is meant to test that any unauthenticated user trying to
        access inventory page should be redirected to login page.
        """
        response = self.client.get("/inventory", follow=True)
        self.assertRedirects(
            response, settings.LOGIN_URL + "login/?" + response.request["QUERY_STRING"]
        )

    def test_authenticated_user_can_access_inventory(self):
        """
        In this test we have logged in using the superuser account and
        trying to access '/inventory' URL and expectation is to be
        able to access it.
        """
        self.client.login(username=self.admin_username, password=self.admin_password)
        response = self.client.get("/inventory", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], "/inventory")

    def test_inventory_search_feature(self):
        """
        In this test we're going to test the search by name or description
        feature as visible on the '/inventory' page.
        """
        self.client.login(username=self.admin_username, password=self.admin_password)

        encoded_search_query = urllib.parse.urlencode({"search": self.inventory.name})
        response = self.client.get(f"/inventory?{encoded_search_query}")
        self.assertEqual(response.status_code, 200)

        root_html = BeautifulSoup(response.content, "lxml")

        # Find first element of td tag which contains the inventory name
        tag = root_html.select_one("td:nth-of-type(1)")

        self.assertEqual(tag.contents[0], self.inventory.name)

    def test_delete_inventory_feature(self):
        """
        In this test we are going to test the delete inventory feature
        used in the '/inventory' page.
        """
        self.client.login(username=self.admin_username, password=self.admin_password)

        response = self.client.delete(f"/inventory?sku={self.inventory.sku}")
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Inventory.objects.all().count() == 0)
