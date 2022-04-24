from django.core.management.base import BaseCommand
import logging

from core.models import Channel
from core.serializers import BaseChannelIDSerializer
import csv

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_list(self, serialzier_data, report_list=[]):
        for srdata in serialzier_data:
            data = (srdata["title"], srdata.get("average_rating").get("rating__avg"))
            report_list.append(data)
            if srdata.get("sub_channels"):
                self.get_list(srdata.get("sub_channels"), report_list)

        return report_list

    def handle(self, *args, **options):
        # logger.info("""
        #     Generate Report Started Please wait...
        # """)
        channels = Channel.objects.filter().prefetch_related("sub_channels")
        serializer = BaseChannelIDSerializer(channels, many=True)
        report_list = self.get_list(serializer.data, [])

        report_list.sort(key=lambda x: x[1], reverse=True)

        with open("report.csv", "w") as file:
            csvwriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(["Title", "Average"])
            csvwriter.writerows(list(report_list))
        # logger.info("SUCCESS")
