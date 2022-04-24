import json

from rest_framework import status
from core.models import Channel
from rest_framework.test import APITestCase


class TestSubChannelApi(APITestCase):
    """
        SubChannel Get Api Test Cases
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = '/api/v1/sub-channel/'
        cls.channel1 = Channel.objects.create(title="Main Title1",  language="lang1")
        cls.channel2 = Channel.objects.create(title="Main Title2",  language="lang2")
        Channel.objects.create(title="Title2",  language="lang2", sub_channel=cls.channel1)
        Channel.objects.create(title="Title3",  language="lang3", sub_channel=cls.channel1)
        Channel.objects.create(title="Title4",  language="lang4", sub_channel=cls.channel2)
        Channel.objects.create(title="Title5",  language="lang5", sub_channel=cls.channel2)

    def test_200_case1(self):
        expected_data = [
            {'title': 'Title2', 'language': 'lang2', 'picture': None},
            {'title': 'Title3', 'language': 'lang3', 'picture': None}
        ]
        url = f"{self.url}{self.channel1.id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_data = json.loads(json.dumps(response.data))
        for data in res_data:
            del data["id"]
        self.assertEqual(res_data, expected_data)

    def test_200_case2(self):
        expected_data = [
            {'title': 'Title4', 'language': 'lang4', 'picture': None},
            {'title': 'Title5', 'language': 'lang5', 'picture': None}
        ]
        url = f"{self.url}{self.channel2.id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_data = json.loads(json.dumps(response.data))
        for data in res_data:
            del data["id"]
        self.assertEqual(res_data, expected_data)

    def test_204_case(self):
        url = f"{self.url}99"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_405_case_post(self):
        url = f"{self.url}{self.channel1.id}"
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_405_case_patch(self):
        url = f"{self.url}{self.channel1.id}"
        response = self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_405_case_delete(self):
        url = f"{self.url}{self.channel1.id}"
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @classmethod
    def tearDownClass(cls) -> None:
        Channel.objects.all().delete()
        return super().tearDownClass()
