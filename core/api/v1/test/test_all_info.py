import json
from random import random

from rest_framework import status
from core.models import Channel
from core.models import Content
from rest_framework.test import APITestCase


class TestAllInforApi(APITestCase):
    """
        Channels and Contents Get Api Test Cases
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = '/api/v1/all-info/'

    def prepare_db(self):
        self.channel1 = Channel.objects.create(title="Main Title1",  language="lang1")
        self.channel2 = Channel.objects.create(title="Main Title2",  language="lang2")
        self.subchannel2 = Channel.objects.create(title="Title2",  language="lang2", sub_channel=self.channel1)
        self.subchannel3 = Channel.objects.create(title="Title3",  language="lang3", sub_channel=self.channel1)
        self.subchannel4 = Channel.objects.create(title="Title4",  language="lang4", sub_channel=self.channel2)
        self.subchannel5 = Channel.objects.create(title="Title5",  language="lang5", sub_channel=self.channel2)
        self.content1 = Content.objects.create(
            content_type="Text", url="some_fake_url1", content_description="fake_desc", authors="fake_author",
            genre="genre", rating=8, channel=self.subchannel2)
        self.content2 = Content.objects.create(
            content_type="Video", url="some_fake_url2", content_description="fake_desc", authors="fake_author",
            genre="genre", rating=8, channel=self.subchannel2)
        Content.objects.create(content_type="File", url="some_fake_url3", content_description="fake_desc",
                               authors="fake_author1", genre="genre", rating=7, channel=self.subchannel2)
        Content.objects.create(content_type="File", url="some_fake_url4", content_description="fake_desc",
                               authors="fake_author2", genre="genre", rating=6, channel=self.subchannel3)
        Content.objects.create(content_type="File", url="some_fake_url5", content_description="fake_desc",
                               authors="fake_author3", genre="genre", rating=10, channel=self.subchannel4)
        Content.objects.create(content_type="File", url="some_fake_url6", content_description="fake_desc",
                               authors="fake_author4", genre="genre", rating=3, channel=self.subchannel5)

    def test_200_case1(self):
        self.prepare_db()
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_data = json.loads(json.dumps(response.data))
        for data in res_data:
            if data.get("id") == self.channel1.id:
                subchannels = data.get("sub_channels")
                for subchannel in subchannels:
                    if subchannel.get("id") == self.subchannel2.id:
                        self.assertEqual(subchannel.get('title'), self.subchannel2.title)
                        self.assertEqual(subchannel.get('language'), self.subchannel2.language)
                        self.assertEqual(len(subchannel.get('contents')), 3)
                self.assertEqual(data.get("title"), self.channel1.title)
                self.assertEqual(data.get("language"), self.channel1.language)

    def test_204_case(self):
        Content.objects.all().delete()
        Channel.objects.all().delete()
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
        Content.objects.all().delete()
        Channel.objects.all().delete()
        return super().tearDownClass()
