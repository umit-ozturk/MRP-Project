from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, schema
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from api.v1.schemas import HelloSchema, RegisterSchema, LoginSchema
from api.v1.tools import create_profile, check_user_is_valid
from profile.serializers import UserProfileSerializer


@api_view(['GET'])
@schema(HelloSchema, )
def hello(request):
    """
    API endpoint that just hello world.
    """
    try:
        email = request.data["email"]
        return Response({"message": "Hello World", "data": email}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@schema(RegisterSchema, )
def register_view(request):
    """
    API endpoint that allows users to register.
    """
    try:
        user = create_profile(request.user, request.data)
        return Response({"detail": "Üyelik başarıyla oluşturuldu."}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@schema(LoginSchema, )
def login_view(request):
    """
    API endpoint that allows users to login.
    """
    try:
        user = authenticate(username=request.data["email"], password=request.data["password"])
        check_user_is_valid(user, **request.data)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, 'user': UserProfileSerializer(user).data}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
