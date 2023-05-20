from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ...constant import GET,POST,PUT,DELETE
from ...models import Homework,HomeworkChannel,HomeworkFile,HomeworkAccessFileAccount
from rest_framework import status
from django.forms.models import model_to_dict
from ...serializers.docket import *
from decouple import config

DELTA_TIME_SECOND = int(config("DELTA_TIME_SECOND"))

@api_view([POST])
def create_homework(request,discord_id:str,channel_id:str):
    channel = HomeworkChannel.objects.get(channel_id=channel_id)
    file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
    if file.owner_id != str(discord_id) and not channel.can_edit:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        timestamp = datetime(
            request.data["year"],
            request.data["month"],
            request.data["date"],
            23,59,59
        )
    except:
        return Response({"message": "Invalid date"},status=status.HTTP_400_BAD_REQUEST)
    finalTimestamp = int(timestamp.timestamp()) + DELTA_TIME_SECOND
    homework = Homework(
        file_id=file,
        timestamp = finalTimestamp,
        day_name = timestamp.strftime("%A"),
        **request.data
    )
    print("Homework",homework.timestamp)
    homework.save()
    print("Homework",homework.timestamp)
    return Response(model_to_dict(homework),status=status.HTTP_201_CREATED)

@api_view([GET])
def all_homework_in_file(request,channel_id:str):
    try:
        htype = request.query_params.get('type','ALL')
        currentTimestamp = int(datetime.now().timestamp())
        file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
        homework = Homework.objects.filter(file_id=file,timestamp__gte=currentTimestamp)
        totalHomework = len(homework)
        filteredHomework = len(homework)
        if htype != "ALL":
            homework = homework.filter(type=htype)
            filteredHomework = len(homework)
        return Response({
            "file": model_to_dict(file),
            "total_homework_count": totalHomework,
            "type_homework_count": filteredHomework,
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

        try:
            timestamp = datetime(
            homework.year,
            homework.month,
            homework.date,
            23,59,59
        )
        except:
            return Response({"message": "Invalid date"},status=status.HTTP_400_BAD_REQUEST)

        homework.timestamp = int(timestamp.timestamp()) + DELTA_TIME_SECOND
        homework.day_name = timestamp.strftime("%A")

        homework.save()
        return Response(model_to_dict(homework),status=status.HTTP_200_OK)
    elif request.method == DELETE:
        homework.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)