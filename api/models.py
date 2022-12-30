from django.db import models
# Discord Message

class DiscordMessage(models.Model):
    message_id = models.IntegerField(primary_key=True)
    discord_id = models.IntegerField()
    channel_id = models.IntegerField()
    username = models.CharField(max_length=50)
    content = models.CharField(max_length=10000)
    datetime = models.DateTimeField(blank=True,auto_now_add=True)

class DiscordMessageAttachment(models.Model):
    message_id = models.ForeignKey(DiscordMessage,on_delete=models.CASCADE,db_column="message_id")
    url = models.CharField(max_length=1000)

class DiscordMessageEmoji(models.Model):
    message_id = models.ForeignKey(DiscordMessage,on_delete=models.CASCADE,db_column="message_id")
    emoji = models.CharField(max_length=100)

class DiscordMessageMentionChannel(models.Model):
    message_id = models.ForeignKey(DiscordMessage,on_delete=models.CASCADE,db_column="message_id")
    channel = models.CharField(max_length=100)

class DiscordMessageMentionRole(models.Model):
    message_id = models.ForeignKey(DiscordMessage,on_delete=models.CASCADE,db_column="message_id")
    role = models.CharField(max_length=100)

class DiscordMessageMentionUser(models.Model):
    message_id = models.ForeignKey(DiscordMessage,on_delete=models.CASCADE,db_column="message_id")
    user = models.CharField(max_length=100)

# Homeworklist

class HomeworkFile(models.Model):
    file_id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Homework(models.Model):
    homework_id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(HomeworkFile,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True,blank=True)
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    timestamp = models.IntegerField()
    day_name = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    label = models.CharField(max_length=2000)

class HomeworkChannel(models.Model):
    channel_id = models.IntegerField(primary_key=True)
    file_id = models.ForeignKey(HomeworkFile,on_delete=models.CASCADE)
    enable_notification = models.BooleanField(default=False)