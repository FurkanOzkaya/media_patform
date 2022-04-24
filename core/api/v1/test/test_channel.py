import json

from rest_framework import status
from core.models import Channel
from rest_framework.test import APITestCase


class TestChannelApi(APITestCase):
    """
        Channel Get Api Test Cases
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = '/api/v1/channel/'

    def prepare_data(self):
        channel1 = Channel.objects.create(title="Title1",  language="lang1")
        Channel.objects.create(title="Title2",  language="lang2")
        Channel.objects.create(title="Title3",  language="lang3")
        Channel.objects.create(title="Title4",  language="lang4", sub_channel=channel1)

    def test_200_case1(self):
        self.prepare_data()
        expected_data = [
            {'title': 'Title1', 'language': 'lang1', 'picture': None},
            {'title': 'Title2', 'language': 'lang2', 'picture': None},
            {'title': 'Title3', 'language': 'lang3', 'picture': None}
        ]
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_data = json.loads(json.dumps(response.data))
        for data in res_data:
            del data["id"]
        self.assertEqual(res_data, expected_data)

    def test_204_case(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_405_case_post(self):
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_405_case_patch(self):
        response = self.client.patch(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_405_case_delete(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @classmethod
    def tearDownClass(cls) -> None:
        Channel.objects.all().delete()
        return super().tearDownClass()
