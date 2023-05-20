from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ...constant import GET,POST,PUT,DELETE
from ...models import Homework,HomeworkChannel,HomeworkFile,HomeworkAccessFileAccount
from rest_framework import status
from django.forms.models import model_to_dict
from ...serializer import *

@api_view([GET])
def all_channel(request):
    channels = HomeworkChannel.objects.all()
    
    serializes = HomeworkChannelSerializer(channels,many=True)
    
    return Response({'channels': serializes.data})

@api_view([PUT])
def open_file(request,discord_id:str,channel_id:str,file_id:int):
    file = HomeworkFile.objects.get(file_id=file_id)
    try:
        channel = HomeworkChannel.objects.get(channel_id=channel_id)
        channel.file_id = file
        channel.can_edit = False
        channel.save()
        return Response({
            "file": model_to_dict(file),
            "channel": model_to_dict(channel)
        },status=status.HTTP_200_OK)
    except HomeworkChannel.DoesNotExist:
        channel = HomeworkChannel(
            channel_id=channel_id,
            file_id=file
        )
        channel.save()
        return Response({
            "file": model_to_dict(file),
            "channel": model_to_dict(channel)
        },status=status.HTTP_201_CREATED)

@api_view([PUT])
def manage_channel(request,discord_id:str,channel_id:str):
    try:
        file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
        if 'can_edit' in request.data and file.owner_id != discord_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        channel = HomeworkChannel.objects.get(channel_id=channel_id)
        channel.enable_notification = request.data.get('enable_notification',channel.enable_notification)
        channel.can_edit = request.data.get('can_edit',channel.can_edit)
        channel.save()
        return Response(model_to_dict(channel),status=status.HTTP_200_OK)
    except HomeworkFile.DoesNotExist:
        return Response({"message": "This channel has not selected file yet"},status=status.HTTP_400_BAD_REQUEST)
