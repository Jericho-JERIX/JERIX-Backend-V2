from ..models import *
from rest_framework import serializers

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        models = Homework
        fields = "__all__"

class HomeworkFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkFile
        fields = "__all__"

class HomeworkChannelSerializer(serializers.ModelSerializer):
    file_id = HomeworkFileSerializer()
    class Meta:
        model = HomeworkChannel
        fields = "__all__"