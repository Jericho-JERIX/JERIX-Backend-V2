from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constant import GET,POST,PUT,DELETE
from rest_framework import status

@api_view([GET])
def greeting(request):
    return Response({"message": "Welcome to JERIX-Backend V2!"},status=status.HTTP_200_OK)