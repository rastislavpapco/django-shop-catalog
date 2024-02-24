import json
import os
from django.apps import apps
from django.test import TestCase, Client
from .models import AttributeName


__dir_location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class YourTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        # Delete all model objects after each test
        for model in apps.get_models():
            model.objects.all().delete()

    def test_upload_data(self):
        data = json.load(open(os.path.join(__dir_location__, "../test_data.json"), "r", encoding="utf-8"))
        response = self.client.post('/catalog/upload/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_upload_data_invalid_model_name(self):
        invalid_data = [{"InvalidAttribute": {"id": 1, "name": "Invalid"}}]
        response = self.client.post('/catalog/upload/', invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_model_entry(self):
        # Create a sample object
        AttributeName.objects.create(id=1, name="Size", code="SZ", show=False)

        response = self.client.get(f'/catalog/AttributeName/1/')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["AttributeName"]["name"], "Size")

    def test_get_model_entry_invalid_model_name(self):
        response = self.client.get(f'/catalog/InvalidModelName/1/')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data["Message"], "Could not find model class for InvalidModelName.")

    def test_get_model_entry_invalid_entry_id(self):
        # Create a sample object
        AttributeName.objects.create(id=1, name="Size", code="SZ", show=False)

        response = self.client.get(f'/catalog/AttributeName/2/')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data["Message"], "Could not find AttributeName with id 2")

    def test_get_all_model_entries(self):
        # Create a sample objects
        AttributeName.objects.create(id=1, name="Size", code="SZ", show=False)
        AttributeName.objects.create(id=2, name="Colour", code="CLR", show=True)

        response = self.client.get('/catalog/AttributeName/')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data["AttributeNames"]), 2)

    def test_get_all_model_entries_empty(self):
        response = self.client.get('/catalog/AttributeName/')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data["AttributeNames"]), 0)
