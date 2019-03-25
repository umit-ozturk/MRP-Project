from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, schema, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from api.v1.schemas import RegisterSchema, LoginSchema, RawInfoSchema, ProductInfoSchema
from api.v1.tools import create_profile, check_user_is_valid
from profile.serializers import UserProfileSerializer
from stock.serializers import ProductStockSerializer, RawStockSerializer
from product.serializers import ProductSerializer, RawSerializer
from stock.models import ProductStock, RawStock
from product.models import Product, Raw


@api_view(['GET'])
def test_view(request):
    """
    API endpoint that just test.
    """
    try:
        return Response({"message": _("Hello World")}, status=status.HTTP_200_OK)
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
        return Response({"detail": _("Üyelik başarıyla oluşturuldu.")}, status=status.HTTP_200_OK)
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
def list_product_stock_view(request):
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
def list_raw_stock_view(request):
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


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@schema(ProductInfoSchema, )
def list_product_info_view(request):
    """
    API endpoint return product and quantity by product name
    """
    if request.method == "GET":
        try:
            product_info = Product.objects.filter(name=request.GET.get('product_name')).order_by('-created_at')
            if product_info.count() != 0:
                product_info_serializer = ProductSerializer(product_info, many=True)
                return Response(product_info_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Ürün bilgisi bulunamadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@schema(RawInfoSchema, )
def list_raw_info_view(request):
    """
    API endpoint return raw and quantity by raw name
    """
    if request.method == "GET":
        try:
            raw_info = Raw.objects.filter(name=request.GET.get('raw_name')).order_by('-created_at')
            if raw_info.count() != 0:
                raw_info_serializer = RawSerializer(raw_info, many=True)
                return Response(raw_info_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Hammadde bilgisi bulunamadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
