from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ...constant import GET,POST,PUT,DELETE
from ...models import Homework,HomeworkChannel,HomeworkFile,HomeworkAccessFileAccount
from rest_framework import status
from django.forms.models import model_to_dict
from ...serializers.docket import *

@api_view([GET])
def get_general_info(request):
    allHomeworks = Homework.objects.all()
    activeHomeworks = Homework.objects.filter(timestamp__gte=int(datetime.now().timestamp()),is_active=True)
    allChannels = HomeworkChannel.objects.all()
    allFiles = HomeworkFile.objects.all()

    return Response({
        "total_homeworks": len(allHomeworks),
        "total_active_homeworks": len(activeHomeworks),
        "total_channels": len(allChannels),
        "total_files": len(allFiles)
    },status=status.HTTP_200_OK)