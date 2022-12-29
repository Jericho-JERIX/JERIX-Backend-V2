from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constant import GET,POST,PUT,DELETE
from ..models import DiscordMessage,DiscordMessageMentionRole,DiscordMessageAttachment,DiscordMessageEmoji,DiscordMessageMentionChannel,DiscordMessageMentionUser
from rest_framework import status
from django.forms.models import model_to_dict

@api_view([POST])
def create_message(request):
    