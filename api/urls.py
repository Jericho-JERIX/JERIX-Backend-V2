from django.urls import path
from .views import message,homework

urlpatterns = [
    path('message',message.create_message),

    path('homework',),
    path('homework/file/<int:file>',),
    path('homework/',),
    path('homework',),
    
]