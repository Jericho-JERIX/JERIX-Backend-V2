from django.urls import path

from .views.docket import homework,file,channel,statistic
from .views import greeting,message

urlpatterns = [
    path('greeting',greeting.greeting),

    path('message',message.create_message),
    
    path('homeworklist/account/<str:discord_id>/file',file.all_files),
    path('homeworklist/account/<str:discord_id>/file/<int:file_id>',file.manage_file),
    path('homeworklist/account/<str:discord_id>/channel/<str:channel_id>',channel.manage_channel),
    path('homeworklist/account/<str:discord_id>/channel/<str:channel_id>/file',file.create_file),
    path('homeworklist/account/<str:discord_id>/channel/<str:channel_id>/file/<int:file_id>',channel.open_file),
    path('homeworklist/account/<str:discord_id>/channel/<str:channel_id>/homework',homework.create_homework),
    path('homeworklist/account/<str:discord_id>/channel/<str:channel_id>/homework/<int:homework_id>',homework.manage_homework),
    path('homeworklist/account/<str:discord_id>/channel/<str:channel_id>/homework/<int:homework_id>/check',homework.check_homework),
    path('homeworklist/channel/<str:channel_id>',homework.all_homework_in_file),
    path('homeworklist/channel',channel.all_channel),
    path('homeworklist/statistic/general',statistic.get_general_info)
]

# - ดูไฟล์ทั้งหมด discord_id
# - สร้างไฟล์ discord_id,channel_id
# - เปิดไฟล์ discord_id,channel_id,file_id
# - แก้ไขไฟล์ discord_id,file_id,file_id
# - ลบไฟล์ discord_id,file_id,file_id
# - สร้างการบ้าน discord_id,channel_id
# - แก้ไขการบ้าน discord_id,channel_id,homework_id
# - ลบการบ้าน discord_id,channel_id,homework_id
