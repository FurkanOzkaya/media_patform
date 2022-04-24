from core.models import Channel, Content
from rest_framework import serializers


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ChannelSerializer(serializers.ModelSerializer):
    sub_channels = RecursiveField(many=True)
    contents = ContentSerializer(many=True)

    class Meta:
        model = Channel
        exclude = ["sub_channel"]


class BaseChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        exclude = ["sub_channel"]


class BaseContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = '__all__'


class BaseChannelIDSerializer(serializers.ModelSerializer):
    sub_channels = RecursiveField(many=True)
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.average_rating

    class Meta:
        model = Channel
        fields = ["id", "title", "sub_channels", "average_rating"]
