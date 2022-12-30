from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constant import GET,POST,PUT,DELETE
from ..models import DiscordMessage,DiscordMessageMentionRole,DiscordMessageAttachment,DiscordMessageEmoji,DiscordMessageMentionChannel,DiscordMessageMentionUser
from rest_framework import status
from django.forms.models import model_to_dict

@api_view([POST])
def create_message(request):
    message = DiscordMessage(**request.data['message'])
    message.save()

    for instance in request.data['extension']['attachments']:
        extended = DiscordMessageAttachment(message_id=message,url=instance)
        extended.save()

    for instance in request.data['extension']['emoji']:
        extended = DiscordMessageEmoji(message_id=message,emoji=instance)
        extended.save()
    
    for instance in request.data['extension']['mentions_channel']:
        extended = DiscordMessageMentionChannel(message_id=message,channel=instance)
        extended.save()
    
    for instance in request.data['extension']['mentions_role']:
        extended = DiscordMessageMentionRole(message_id=message,role=instance)
        extended.save()
    
    for instance in request.data['extension']['mentions_user']:
        extended = DiscordMessageMentionUser(message_id=message,user=instance)
        extended.save()

    return Response(model_to_dict(message))