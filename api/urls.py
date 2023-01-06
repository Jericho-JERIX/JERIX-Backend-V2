from django.urls import path
from .views import message,homework

urlpatterns = [
    path('message',message.create_message),

    path('homeworklist/account/<int:discord_id>/file',homework.all_files),
    path('homeworklist/account/<int:discord_id>/file/<int:file_id>',homework.manage_file),
    path('homeworklist/account/<int:discord_id>/channel/<int:channel_id>',homework.manage_channel),
    path('homeworklist/account/<int:discord_id>/channel/<int:channel_id>/file',homework.create_file),
    path('homeworklist/account/<int:discord_id>/channel/<int:channel_id>/file/<int:file_id>',homework.open_file),
    path('homeworklist/account/<int:discord_id>/channel/<int:channel_id>/homework',homework.create_homework),
    path('homeworklist/account/<int:discord_id>/channel/<int:channel_id>/homework/<int:homework_id>',homework.manage_homework),
    path('homeworklist/channel/<int:channel_id>',homework.all_homework_in_file),
]

# - ดูไฟล์ทั้งหมด discord_id
# - สร้างไฟล์ discord_id,channel_id
# - เปิดไฟล์ discord_id,channel_id,file_id
# - แก้ไขไฟล์ discord_id,file_id,file_id
# - ลบไฟล์ discord_id,file_id,file_id
# - สร้างการบ้าน discord_id,channel_id
# - แก้ไขการบ้าน discord_id,channel_id,homework_id
# - ลบการบ้าน discord_id,channel_id,homework_id
