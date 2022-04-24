

from rest_framework import serializers


class SubChannelPathSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        help_text="Id Of Main Channel")

    def validate(self, attrs):
        return super().validate(attrs)


class ContentsPathSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="Id of Sub Channel/ Channel Which has contents")

    def validate(self, attrs):
        return super().validate(attrs)
