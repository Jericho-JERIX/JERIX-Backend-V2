from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ...constant import GET,POST,PUT,DELETE
from ...models import *
from rest_framework import status
from django.forms.models import model_to_dict
from ...serializers.docket import *

Months = [
    "january",
    "febuary",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december"
]

@api_view([GET])
def search_homework(request,channel_id:str):
    homeworks = Homework.objects.filter(file_id__homeworkchannel__channel_id=channel_id)
    print([model_to_dict(i) for i in homeworks])
    
    keywords = request.data["keyword"]

    related_label = homeworks.filter(label__icontains=keywords)
    related_type = homeworks.filter(type__icontains=keywords)
    related_dayname = homeworks.filter(day_name__icontains=keywords)

    try:
        related_date = homeworks.filter(date=keywords)
    except:
        related_date = homeworks.filter(date=-1)

    try:
        related_month = homeworks.filter(month=keywords)
    except:
        month_number = -1
        for i in range(len(Months)):
            if keywords.lower() in Months[i]:
                month_number = i + 1
                break
        related_month = homeworks.filter(month=month_number)

    related = related_label | related_type | related_date | related_month | related_dayname

    serializes = HomeworkSerializer(related,many=True)
    return Response({'homeworks': serializes.data},status=status.HTTP_200_OK)
    
    
    # === DUBUGGING SESSION === #
    # ser_related_label = HomeworkSerializer(related_label,many=True)    
    # ser_related_type = HomeworkSerializer(related_type,many=True)
    # ser_related_date = HomeworkSerializer(related_date,many=True)
    # ser_related_month = HomeworkSerializer(related_month,many=True)    
    # ser_related_dayname = HomeworkSerializer(related_dayname,many=True)

    # return Response({
    #     "related_label": ser_related_label.data,
    #     "related_type": ser_related_type.data,
    #     "related_dayname": ser_related_dayname.data,
    #     "related_date": ser_related_date.data,
    #     "related_month": ser_related_month.data,
    # },status=status.HTTP_200_OK)