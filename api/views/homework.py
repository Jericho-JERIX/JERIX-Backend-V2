from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constant import GET,POST,PUT,DELETE
from ..models import Homework,HomeworkChannel,HomeworkFile,HomeworkAccessFileAccount
from rest_framework import status
from django.forms.models import model_to_dict

@api_view([GET])
def all_files(request,discord_id:int):
    files = HomeworkFile.objects.filter(owner_id=discord_id)
    files_list = [model_to_dict(i) for i in files]
    return Response(files_list,status=status.HTTP_200_OK)

@api_view([POST])
def create_file(request,discord_id:int,channel_id:int):
    files = HomeworkFile.objects.filter(owner_id=discord_id)
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

@api_view([POST])
def create_homework(request,discord_id:int,channel_id:int):
    file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
    if file.owner_id != discord_id:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    timestamp = datetime(
        request.data["year"],
        request.data["month"],
        request.data["date"],
        23,59,59
    )
    homework = Homework(
        file_id=file,
        timestamp = int(timestamp.timestamp()),
        day_name = timestamp.strftime("%A"),
        **request.data
    )
    homework.save()
    return Response(model_to_dict(homework),status=status.HTTP_201_CREATED)

@api_view([PUT])
def open_file(request,discord_id:int,channel_id:int,file_id:int):
    file = HomeworkFile.objects.get(file_id=file_id)
    channel = HomeworkChannel.objects.get(channel_id=channel_id)
    if file.owner_id != discord_id:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    channel.file_id = file
    channel.save()
    return Response({
        "file": model_to_dict(file),
        "channel": model_to_dict(channel)
    },status=status.HTTP_200_OK)

@api_view([PUT,DELETE])
def manage_file(request,discord_id:int,file_id:int):
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

@api_view([PUT])
def manage_channel(request,discord_id:int,channel_id:int):
    file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
    if file.owner_id != discord_id:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    channel = HomeworkChannel.objects.get(channel_id=channel_id)
    channel.enable_notification = request.data.get('enable_notification',channel.enable_notification)
    channel.visible_only = request.data.get('visible_only',channel.visible_only)
    channel.save()
    return Response(model_to_dict(channel),status=status.HTTP_200_OK)

@api_view([GET])
def all_homework_in_file(request,channel_id:int):
    htype = request.query_params.get('type','ALL')
    file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
    homework = Homework.objects.filter(file_id=file)
    if htype != "ALL":
        homework = homework.filter(type=htype)
    return Response([model_to_dict(i) for i in homework],status=status.HTTP_200_OK)

@api_view([PUT,DELETE])
def manage_homework(request,discord_id:int,channel_id:int,homework_id:int):
    file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
    if file.owner_id != discord_id:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    homework = Homework.objects.get(homework_id=homework_id)

    if request.method == PUT:
        homework.date = request.data.get("date",homework.date)
        homework.month = request.data.get("month",homework.month)
        homework.year = request.data.get("year",homework.year)
        homework.type = request.data.get("type",homework.type)
        homework.label = request.data.get("label",homework.label)

        timestamp = datetime(
            homework.year,
            homework.month,
            homework.date,
            23,59,59
        )

        homework.timestamp = int(timestamp.timestamp())
        homework.day_name = timestamp.strftime("%A")

        homework.save()
        return Response(model_to_dict(homework),status=status.HTTP_200_OK)
    elif request.data == DELETE:
        homework.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)