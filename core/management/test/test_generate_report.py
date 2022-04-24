import os
import csv
import logging

from io import StringIO

from django.conf import settings
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from core.models import Channel, Content


logger = logging.getLogger(__name__)


def mock_func(self, data, report_list):
    raise Exception


class GenerateReportTest(TestCase):
    def call_django_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            "generate_report",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def prepare_data(self):
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

    def test_success_case1(self):
        self.prepare_data()

        out = self.call_django_command()
        self.assertEqual(out, "")
        file_exists = os.path.exists(os.path.join(settings.BASE_DIR, "report.csv"))
        self.assertTrue(file_exists)

    @patch('core.management.commands.generate_report.Command.get_list', mock_func)
    def test_fail_case(self):
        self.prepare_data()
        path = os.path.join(settings.BASE_DIR, "report.csv")

        with self.assertRaises(Exception):
            self.call_django_command()
        file_exists = os.path.exists(path)
        self.assertFalse(file_exists)

    def test_success_case2(self):
        self.prepare_data()

        out = self.call_django_command()
        self.assertEqual(out, "")
        path = os.path.join(settings.BASE_DIR, "report.csv")

        with open(path) as csv_file:
            expected_data = [
                ['Title', 'Average'],
                ['Title4', '10.0'],
                ['Title4', '10.0'],
                ['Title2', '7.666666666666667'],
                ['Title2', '7.666666666666667'],
                ['Main Title1', '6.833333333333334'],
                ['Main Title2', '6.5'],
                ['Title3', '6.0'],
                ['Title3', '6.0'],
                ['Title5', '3.0'],
                ['Title5', '3.0']
            ]
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_data = list(csv_reader)
            csv_data = [x for x in csv_data if x]
            self.assertEqual(csv_data, expected_data)

    def tearDown(self) -> None:
        path = os.path.join(settings.BASE_DIR, "report.csv")
        if os.path.exists(path):
            os.remove(path)
        return super().tearDown()
