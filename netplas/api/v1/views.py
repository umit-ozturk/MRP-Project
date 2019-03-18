from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from rest_framework import status
from api.v1.schemas import HelloSchema, RegisterSchema, LoginSchema
from api.v1.tools import create_profile



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