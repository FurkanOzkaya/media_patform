from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.decarators import validator
from core.api.v1.common.request_serializer import SubChannelPathSerializer
from core.models import Channel

from core.serializers import BaseChannelSerializer


class SubChannelAPI(APIView):
    """
    List all SubChannels of Main Channel
    """
    @validator(path_validator=SubChannelPathSerializer)
    def get(self, _, path_serializer, *args, **kwargs):
        channels = Channel.objects.filter(sub_channel=path_serializer.validated_data.get("id"))
        serializer = BaseChannelSerializer(channels, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
