from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Channel

from core.serializers import BaseChannelSerializer


class ChannelAPI(APIView):
    """
    List Main Channels
    """

    def get(self, _):
        channels = Channel.objects.filter(sub_channel=None)
        serializer = BaseChannelSerializer(channels, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
