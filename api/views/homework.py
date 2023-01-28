from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constant import GET,POST,PUT,DELETE
from ..models import Homework,HomeworkChannel,HomeworkFile,HomeworkAccessFileAccount
from rest_framework import status
from django.forms.models import model_to_dict

@api_view([GET])
def all_files(request,discord_id:str):
    files = HomeworkFile.objects.filter(owner_id=discord_id)
    return Response({
        'files': [model_to_dict(i) for i in files]
    },status=status.HTTP_200_OK)

@api_view([GET])
def all_channel(request):
    channels = HomeworkChannel.objects.all()
    return Response({'channels': [model_to_dict(i) for i in channels]})

@api_view([POST])
def create_file(request,discord_id:str,channel_id:str):
    files = HomeworkFile.objects.filter(owner_id=discord_id)
    if len(files) >= 5:
        return Response({'message': "Exceeded limit!"},status=status.HTTP_403_FORBIDDEN)
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
def create_homework(request,discord_id:str,channel_id:str):
    channel = HomeworkChannel.objects.get(channel_id=channel_id)
    file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
    if file.owner_id != str(discord_id) and not channel.can_edit:
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

@api_view([PUT])
def manage_channel(request,discord_id:str,channel_id:str):
    file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
    if 'can_edit' in request.data and file.owner_id != discord_id:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    channel = HomeworkChannel.objects.get(channel_id=channel_id)
    channel.enable_notification = request.data.get('enable_notification',channel.enable_notification)
    channel.can_edit = request.data.get('can_edit',channel.can_edit)
    channel.save()
    return Response(model_to_dict(channel),status=status.HTTP_200_OK)

@api_view([GET])
def all_homework_in_file(request,channel_id:str):
    try:
        htype = request.query_params.get('type','ALL')
        file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
        homework = Homework.objects.filter(file_id=file)
        if htype != "ALL":
            homework = homework.filter(type=htype)
        return Response({
            "file": model_to_dict(file),
            "homeworks": sorted([model_to_dict(i) for i in homework],key=lambda x: x['timestamp'])
        },status=status.HTTP_200_OK)
    except HomeworkFile.DoesNotExist:
        return Response({"message": "This channel has not selected file yet"},status=status.HTTP_400_BAD_REQUEST)

@api_view([PUT,DELETE])
def manage_homework(request,discord_id:str,channel_id:str,homework_id:int):
    channel = HomeworkChannel.objects.get(channel_id=channel_id)
    file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
    if file.owner_id != str(discord_id) and not channel.can_edit:
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
    elif request.method == DELETE:
        homework.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)