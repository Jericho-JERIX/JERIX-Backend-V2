from django.db import models

# Create your models here.

class DiscordMessage(models.Model):
    message_id=models.IntegerField(primary_key=True)
    discord_id=models.IntegerField()
    channel_id=models.IntegerField()
    username=models.CharField(max_length=50)
    content=models.CharField(max_length=10000)
    timestamp=models.IntegerField()
    datetime=models.DateTimeField(auto_now_add=True)

class DiscordMessageAttachment(models.Model):
    message_id=models.ForeignKey(DiscordMessage,on_delete=models.CASCADE)
    url=models.CharField(max_length=1000)

class DiscordMessageEmoji(models.Model):
    message_id=models.ForeignKey(DiscordMessage,on_delete=models.CASCADE)
    emoji=models.CharField(max_length=100)

class DiscordMessageMentionChannel(models.Model):
    message_id=models.ForeignKey(DiscordMessage,on_delete=models.CASCADE)
    channel=models.CharField(max_length=100)

class DiscordMessageMentionRole(models.Model):
    message_id=models.ForeignKey(DiscordMessage,on_delete=models.CASCADE)
    role=models.CharField(max_length=100)

class DiscordMessageMentionUser(models.Model):
    message_id=models.ForeignKey(DiscordMessage,on_delete=models.CASCADE)
    user=models.CharField(max_length=100)