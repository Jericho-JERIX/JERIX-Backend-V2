from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constant import GET,POST,PUT,DELETE
from ..models import Homework,HomeworkChannel,HomeworkFile
from rest_framework import status
from django.forms.models import model_to_dict