import json
from random import random

from rest_framework import status
from core.models import Channel
from core.models import Content
from rest_framework.test import APITestCase


class TestContentApi(APITestCase):
    """
        Content Get Api Test Cases
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = '/api/v1/contents/'
        channel1 = Channel.objects.create(title="Main Title1",  language="lang1")
        channel2 = Channel.objects.create(title="Main Title2",  language="lang2")
        cls.subchannel2 = Channel.objects.create(title="Title2",  language="lang2", sub_channel=channel1)
        cls.subchannel3 = Channel.objects.create(title="Title3",  language="lang3", sub_channel=channel1)
        cls.subchannel4 = Channel.objects.create(title="Title4",  language="lang4", sub_channel=channel2)
        cls.subchannel5 = Channel.objects.create(title="Title5",  language="lang5", sub_channel=channel2)
        cls.content1 = Content.objects.create(
            content_type="Text", url="some_fake_url1", content_description="fake_desc", authors="fake_author",
            genre="genre", rating=8, channel=cls.subchannel2)
        cls.content2 = Content.objects.create(
            content_type="Video", url="some_fake_url2", content_description="fake_desc", authors="fake_author",
            genre="genre", rating=8, channel=cls.subchannel2)
        Content.objects.create(content_type="File", url="some_fake_url3", content_description="fake_desc",
                               authors="fake_author1", genre="genre", rating=7, channel=cls.subchannel2)
        Content.objects.create(content_type="File", url="some_fake_url4", content_description="fake_desc",
                               authors="fake_author2", genre="genre", rating=6, channel=cls.subchannel3)
        Content.objects.create(content_type="File", url="some_fake_url5", content_description="fake_desc",
                               authors="fake_author3", genre="genre", rating=10, channel=cls.subchannel4)
        Content.objects.create(content_type="File", url="some_fake_url6", content_description="fake_desc",
                               authors="fake_author4", genre="genre", rating=3, channel=cls.subchannel5)

    def test_200_case1(self):
        url = f"{self.url}{self.subchannel2.id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_data = json.loads(json.dumps(response.data))
        for data in res_data:
            if self.content1.id == data.get("id"):
                self.assertEqual(data.get("authors"), self.content1.authors)
                self.assertEqual(data.get("rating"), self.content1.rating)
                self.assertEqual(data.get("rating_count"), 1)

    def test_200_case2(self):
        url = f"{self.url}{self.subchannel2.id}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_data = json.loads(json.dumps(response.data))
        for data in res_data:
            if self.content2.id == data.get("id"):
                self.assertEqual(data.get("authors"), self.content2.authors)
                self.assertEqual(data.get("rating"), self.content2.rating)
                self.assertEqual(data.get("rating_count"), 1)

    def test_204_case(self):
        url = f"{self.url}99"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_405_case_post(self):
        url = f"{self.url}{self.subchannel2.id}"
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_405_case_patch(self):
        url = f"{self.url}{self.subchannel2.id}"
        response = self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_405_case_delete(self):
        url = f"{self.url}{self.subchannel2.id}"
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @classmethod
    def tearDownClass(cls) -> None:
        Content.objects.all().delete()
        Channel.objects.all().delete()
        return super().tearDownClass()
