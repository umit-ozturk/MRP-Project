from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, schema, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from api.v1.schemas import RegisterSchema, LoginSchema, RawInfoSchema, ProductInfoSchema, CreateProductStockSchema, \
    CreateRawStockSchema, CreateProductSchema, CreateRawSchema, CreateClientSchema, CreateSupplierSchema, \
    CreateProductOrederSchema, CreateRawOrederSchema
from api.v1.tools import create_profile, check_user_is_valid
from profile.serializers import UserProfileSerializer
from stock.serializers import ProductStockSerializer, RawStockSerializer
from product.serializers import ProductSerializer, RawSerializer
from stock.models import ProductStock, RawStock
from product.models import Product, Raw
from system.models import Client, Supplier, ProductOrder, RawOrder


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
    API endpoint that return product stock names
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


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateProductStockSchema, )
def create_product_stock_view(request):
    """
    API endpoint that create product stock
    """
    try:
        product_stock = ProductStock(name=request.data)
        product_stock.save()
        return Response({"detail": _("Ürün deposu başarıyla oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def list_raw_stock_view(request):
    """
    API endpoint that return raw stock names
    """
    if request.method == "GET":
        try:
            raw_stock = RawStock.objects.all().order_by('-created_at')
            if raw_stock.count() != 0:
                raw_stock_serializer = RawStockSerializer(raw_stock, many=True)
                return Response(raw_stock_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Daha önce herhangi bir ham madde deposu oluşturulmadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateRawStockSchema, )
def create_raw_stock_view(request):
    """
    API endpoint that create raw stock
    """
    try:
        raw_stock = RawStock(name=request.data)
        raw_stock.save()
        return Response({"detail": _("Ham madde deposu başarıyla oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@schema(ProductInfoSchema, )
def list_product_info_view(request):
    """
    API endpoint that return product and quantity by product name
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


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateProductSchema, )
def create_product_view(request):
    """
    API endpoint that create product
    """
    try:
        quantity = request.data["quantity"]
        if quantity > 0:
            product_stock = ProductStock.objects.get(name=request.data["product_stock_name"])
            product = Product(stock=product_stock, name=request.data["product_name"], quantity=quantity)
            product.save()
            return Response({"detail": _(str(quantity) + " adet ürün başarıyla oluşturuldu.")},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": _("Ürün miktarını doğru giriniz.")}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"detail": _("Ürün deposu bulunamadı.")}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@schema(RawInfoSchema, )
def list_raw_info_view(request):
    """
    API endpoint that return raw and quantity by raw name
    """
    if request.method == "GET":
        try:
            raw_info = Raw.objects.filter(name=request.GET.get('raw_name')).order_by('-created_at')
            if raw_info.count() != 0:
                raw_info_serializer = RawSerializer(raw_info, many=True)
                return Response(raw_info_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Ham madde bilgisi bulunamadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateRawSchema, )
def create_raw_view(request):
    """
    API endpoint that create raw
    """
    try:
        quantity = request.data["quantity"]
        if int(quantity) > 0:
            raw_stock = RawStock.objects.get(name=request.data["raw_stock_name"])
            raw = Raw(stock=raw_stock, name=request.data["raw_name"], quantity=int(quantity))
            raw.save()
            return Response({"detail": _(str(quantity) + " adet ham madde başarıyla oluşturuldu.")},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": _("Ham madde miktarını doğru giriniz.")}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"detail": _("Ham madde deposu bulunamadı.")}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateClientSchema, )
def create_client_view(request):
    """
    API endpoint that create client
    """
    try:
        client = Client(email=request.data["email"], name=request.data["name"], surname=request.data["surname"],
                        phone=request.data["phone"])
        client.save()
        return Response({"detail": _("Müşteri başarı ile oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateSupplierSchema, )
def create_supplier_view(request):
    """
    API endpoint that create supplier
    """
    try:
        supplier = Supplier(email=request.data["email"], name=request.data["name"], surname=request.data["surname"],
                            phone=request.data["phone"])
        supplier.save()
        return Response({"detail": _("Tedarikçi başarı ile oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateProductOrederSchema, )
def create_product_order_view(request):  # Testing doesnt not yet.
    """
    API endpoint that create product order
    """
    try:
        client = Client.objects.get(email=request.data["client"])
        product_order = ProductOrder(client=client, name=request.data["name"], quantity=request.data["quantity"])
        product_order.save()
        return Response({"detail": _("Tedarikçi başarı ile oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateRawOrederSchema, )
def create_raw_order_view(request): # Testing doesnt not yet.
    """
    API endpoint that create raw order
    """
    try:
        supplier = Supplier.objects.get(email=request.data["supplier"])
        raw_order = RawOrder(supplier=supplier,  name=request.data["name"], quantity=request.data["quantity"])
        raw_order.save()
        return Response({"detail": _("Tedarikçi başarı ile oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class RawUpdateAPIView(UpdateAPIView):
    serializer_class = RawSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch')
    schema = CreateRawSchema
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = Raw.objects.all()


class ProductUpdateAPIView(UpdateAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch')
    schema = CreateProductSchema
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Product.objects.all()