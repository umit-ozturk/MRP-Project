from rest_framework.response import Response
from rest_framework import status
from api.v1.schemas import HelloSchema
from rest_framework.decorators import api_view, schema


@api_view(['POST'])
@schema(HelloSchema, )
def hello(request):
    """
    API endpoint that just hello world.
    """
    try:
        return Response({"message", "Hello World"}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
