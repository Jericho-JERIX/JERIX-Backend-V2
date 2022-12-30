from django.urls import path
from .views import message

urlpatterns = [
    path('message',message.create_message),

    path('homework',),
    path('homework/<int:homework_id>',),
    path('homework',),
    path('homework',),
    
]