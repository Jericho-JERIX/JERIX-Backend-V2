from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ...constant import GET,POST,PUT,DELETE
from ...models import Homework,HomeworkChannel,HomeworkFile,HomeworkAccessFileAccount
from rest_framework import status
from django.forms.models import model_to_dict
from ...serializer import *

@api_view([GET])
def all_files(request,discord_id:str):
    files = HomeworkFile.objects.filter(owner_id=discord_id)
    return Response({
        'files': [model_to_dict(i) for i in files]
    },status=status.HTTP_200_OK)

@api_view([POST])
def create_file(request,discord_id:str,channel_id:str):
    files = HomeworkFile.objects.filter(owner_id=discord_id)
    # if len(files) >= 5:
        # return Response({'message': "Exceeded limit!"},status=status.HTTP_403_FORBIDDEN)
    files_list = [model_to_dict(i) for i in files]
    request.data['filename'] = request.data['filename'].lower().replace(' ','-')
    if request.data['filename'] in [i['filename'] for i in files_list]:
        return Response({'message':"This name has already created!"},status=status.HTTP_406_NOT_ACCEPTABLE)
    file = HomeworkFile(owner_id=discord_id,**request.data)
    file.save()
    channel = HomeworkChannel(
        channel_id=channel_id,
        file_id=file
    )
    channel.save()
    return Response({
        "file": model_to_dict(file),
        "channel": model_to_dict(channel)
    },status=status.HTTP_201_CREATED)

@api_view([PUT,DELETE])
def manage_file(request,discord_id:str,file_id:int):
    file = HomeworkFile.objects.get(file_id=file_id)
    if file.owner_id != discord_id:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == PUT:
        files = HomeworkFile.objects.filter(owner_id=discord_id)
        files_list = [model_to_dict(i) for i in files]
        request.data['filename'] = request.data['filename'].lower().replace(' ','-')

        if request.data['filename'] in [i['filename'] for i in files_list if i['file_id'] != file_id]:
            return Response({'message':"This name has already created!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        file.filename = request.data.get("filename",file.filename)
        file.save()
        return Response(model_to_dict(file),status=status.HTTP_200_OK)
    elif request.method == DELETE:
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)