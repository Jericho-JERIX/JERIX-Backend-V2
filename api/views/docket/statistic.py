from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ...constant import GET,POST,PUT,DELETE
from ...models import Homework,HomeworkChannel,HomeworkFile,HomeworkAccessFileAccount
from rest_framework import status
from django.forms.models import model_to_dict
from ...serializer import *

def get_general_info(request):
    homeworks = Homework.objects.filter(timestamp__gte=int(datetime.now().timestamp()),is_active=True)