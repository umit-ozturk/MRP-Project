from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, schema, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from api.v1.schemas import HelloSchema, RegisterSchema, LoginSchema
from api.v1.tools import create_profile, check_user_is_valid
from profile.serializers import UserProfileSerializer
from stock.serializers import ProductStockSerializer, RawStockSerializer
from stock.models import ProductStock, RawStock


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


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def list_product_stock(request):
    """
    API endpoint return product stock names
    """
    if request.method == "GET":
        try:
            product_stock = ProductStock.objects.all().order_by('-created_at')
            if product_stock.count() != 0:
                product_stock_serializer = ProductStockSerializer(product_stock, many=True)
                return Response(product_stock_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Daha önce herhangi bir ürün deposu oluşturulmadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def list_raw_stock(request):
    """
    API endpoint return raw stock names
    """
    if request.method == "GET":
        try:
            raw_stock = RawStock.objects.all().order_by('-created_at')
            if raw_stock.count() != 0:
                raw_stock_serializer = RawStockSerializer(raw_stock, many=True)
                return Response(raw_stock_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Daha önce herhangi bir hammadde deposu oluşturulmadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

