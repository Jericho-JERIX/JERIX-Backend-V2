from django.db import models

class DiscordAccount(models.Model):
    discord_id = models.CharField(max_length=20,primary_key=True)
    username = models.CharField(max_length=100)

# Discord Message

class DiscordMessage(models.Model):
    message_id = models.CharField(max_length=20,primary_key=True)
    discord_id = models.CharField(max_length=20,)
    channel_id = models.CharField(max_length=20,)
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
    owner_id = models.CharField(max_length=20,)
    filename = models.CharField(max_length=100)

class Homework(models.Model):
    homework_id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(HomeworkFile,on_delete=models.CASCADE,db_column="file_id")
    is_active = models.BooleanField(default=True,blank=True)
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    timestamp = models.IntegerField()
    day_name = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    label = models.CharField(max_length=2000)
    no_deadline = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)

class HomeworkChannel(models.Model):
    channel_id = models.CharField(max_length=20,primary_key=True)
    file_id = models.ForeignKey(HomeworkFile,on_delete=models.CASCADE,db_column="file_id")
    can_edit = models.BooleanField(default=False)
    enable_notification = models.BooleanField(default=False)

class HomeworkAccessFileAccount(models.Model):
    file_id = models.ForeignKey(HomeworkFile,on_delete=models.CASCADE,db_column="file_id")
    discord_id = models.CharField(max_length=20,)