from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Channel

from core.serializers import ChannelSerializer


class AllInfoAPI(APIView):
    """
    List all Channel and  Contents informations with sub_channels
    """

    def get(self, _, format=None):
        channel_contents = Channel.objects.filter(
            sub_channel=None).prefetch_related("sub_channels", "contents")
        serializer = ChannelSerializer(channel_contents, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
