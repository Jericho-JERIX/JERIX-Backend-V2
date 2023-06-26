from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ...constant import GET,POST,PUT,DELETE
from ...models import Homework,HomeworkChannel,HomeworkFile,HomeworkAccessFileAccount
from rest_framework import status
from django.forms.models import model_to_dict
from ...serializers.docket import *
from decouple import config
from django.db.models import Q
from ...utilities.yearDecider import yearDecider

DELTA_TIME_SECOND = int(config("DELTA_TIME_SECOND"))
MAX_TIMESTAMP = 9999999999

@api_view([POST])
def create_homework(request,discord_id:str,channel_id:str):
    channel = HomeworkChannel.objects.get(channel_id=channel_id)
    file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
    if file.owner_id != str(discord_id) and not channel.can_edit:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    if "date" not in request.data or "month" not in request.data or "year" not in request.data:

        homework = Homework(
            file_id=file,
            date=0,
            month=0,
            year=0,
            timestamp = MAX_TIMESTAMP,
            day_name = "Sunday",
            no_deadline = True,
            **request.data
        )
        homework.save()

        serialize = HomeworkSerializer(homework)
        return Response(serialize.data,status=status.HTTP_201_CREATED)
    
    else:
        try:
            decidedYear = yearDecider(request.data["date"],request.data["month"])
            timestamp = datetime(
                decidedYear,
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
            date = request.data["date"],
            month = request.data["month"],
            type = request.data["type"],
            label =  request.data["label"], 
            year = decidedYear
        )

        homework.save()
        return Response(model_to_dict(homework),status=status.HTTP_201_CREATED)

@api_view([GET])
def all_homework_in_file(request,channel_id:str):
    try:
        htype = request.query_params.get('type','ALL')
        currentTimestamp = int(datetime.now().timestamp())
        file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
        homework = Homework.objects.filter(file_id=file,timestamp__gte=currentTimestamp)
        # noDeadlineHomework = homework.filter(no_deadline=True)

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

        if request.data.get("no_deadline",False):
            homework.no_deadline = True 
            homework.timestamp = MAX_TIMESTAMP
        elif homework.no_deadline and "date" not in request.data and "month" not in request.data:
            pass
        else:
            # try:
            if homework.no_deadline and (("date" in request.data and "month" not in request.data) or ("date" not in request.data and "month" in request.data)):
                raise Exception()

            print('pass')
            homework.date = request.data.get("date",homework.date)
            homework.month = request.data.get("month",homework.month)

            decidedYear = yearDecider(homework.date,homework.month)
            
            homework.year = decidedYear

            print(homework.date,homework.month,homework.year)

            timestamp = datetime(
            homework.year,
            homework.month,
            homework.date,
            23,59,59
            )

            # except:
            #     return Response({"message": "Invalid date"},status=status.HTTP_400_BAD_REQUEST)

            homework.no_deadline = False
            homework.timestamp = int(timestamp.timestamp()) + DELTA_TIME_SECOND
            homework.day_name = timestamp.strftime("%A")

        homework.is_checked = False
        homework.type = request.data.get("type",homework.type)
        homework.label = request.data.get("label",homework.label)
        homework.save()
        return Response(model_to_dict(homework),status=status.HTTP_202_ACCEPTED)
    elif request.method == DELETE:
        homework.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view([PUT])
def check_homework(request,discord_id:str,channel_id:str,homework_id:int):
    channel = HomeworkChannel.objects.get(channel_id=channel_id)
    file = HomeworkFile.objects.get(homeworkchannel__channel_id=channel_id)
    
    if file.owner_id != str(discord_id) and not channel.can_edit:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    homework = Homework.objects.get(homework_id=homework_id)

    homework.is_checked = request.data["is_checked"]

    homework.save()
    serialize = HomeworkSerializer(homework)
    return Response(serialize.data,status=status.HTTP_202_ACCEPTED)
