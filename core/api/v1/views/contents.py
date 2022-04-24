from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.decarators import validator
from core.api.v1.common.request_serializer import ContentsPathSerializer
from core.models import Content

from core.serializers import BaseContentSerializer


class ContentsAPI(APIView):
    """
    List all Contents of a Channel
    """
    @validator(path_validator=ContentsPathSerializer)
    def get(self, _, path_serializer, *args, **kwargs):
        contents = Content.objects.filter(channel=path_serializer.validated_data.get("id"))
        serializer = BaseContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
