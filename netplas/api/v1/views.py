from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, schema, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from api.v1.schemas import RegisterSchema, LoginSchema, RawInfoSchema, ProductInfoSchema, CreateProductStockSchema, \
    CreateRawStockSchema, CreateProductSchema, CreateRawSchema, CreateClientSchema, CreateSupplierSchema, \
    CreateProductOrderSchema, CreateRawOrderSchema
from api.v1.tools import create_profile, check_user_is_valid
from profile.serializers import UserProfileSerializer
from stock.serializers import ProductStockSerializer, RawStockSerializer
from product.serializers import ProductSerializer, RawSerializer
from stock.models import ProductStock, RawStock
from product.models import Product, Raw
from system.models import Client, Supplier, ProductOrder, RawOrder, Budget
from system.serializers import ClientSerializer, SupplierSerializer, ProductOrderSerializer, RawOrderSerializer, \
    BudgetSerializer


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


class ProductStockUpdateAPIView(UpdateAPIView):
    serializer_class = ProductStockSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put',)
    schema = CreateProductStockSchema
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = ProductStock.objects.all()


class ProductStockDeleteAPIView(DestroyAPIView):
    serializer_class = ProductStockSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = ProductStock.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": _("Ürün deposu başarıyla kaldırıldı.")}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": _("Ürün deposu bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


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


class RawStockUpdateAPIView(UpdateAPIView):
    serializer_class = RawStockSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put',)
    schema = CreateRawStockSchema
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = RawStock.objects.all()


class RawStockDeleteAPIView(DestroyAPIView):
    serializer_class = RawStockSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = RawStock.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": _("Ham madde deposu başarıyla kaldırıldı.")}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": _("Ham madde deposu bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


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
        return Response({"detail": _("Ürün deposu bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateAPIView(UpdateAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put',)
    schema = CreateProductSchema
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Product.objects.all()


class ProductDeleteAPIView(DestroyAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Product.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": _("Ürün başarıyla kaldırıldı.")}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": _("Ürün bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


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


class RawUpdateAPIView(UpdateAPIView):
    serializer_class = RawSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put',)
    schema = CreateRawSchema
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = Raw.objects.all()


class RawDeleteAPIView(DestroyAPIView):
    serializer_class = RawSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Raw.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": _("Ham madde başarıyla kaldırıldı.")}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": _("Ham madde bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def list_client_view(request):
    """
    API endpoint that return client information
    """
    if request.method == "GET":
        try:
            client = Client.objects.all().order_by('-created_at')
            if client.count() != 0:
                client_serializer = ClientSerializer(client, many=True)
                return Response(client_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Daha önce herhangi bir müşteri oluşturulmadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
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


class ClientUpdateAPIView(UpdateAPIView):
    serializer_class = ClientSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put',)
    schema = CreateClientSchema
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Client.objects.all()


class ClientDeleteAPIView(DestroyAPIView):
    serializer_class = ClientSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Client.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": _("Müşteri bilgileri başarıyla kaldırıldı.")}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": _("Müşteri bilgileri bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def list_supplier_view(request):
    """
    API endpoint that return supplier information
    """
    if request.method == "GET":
        try:
            supplier = Supplier.objects.all().order_by('-created_at')
            if supplier.count() != 0:
                supplier_serializer = SupplierSerializer(supplier, many=True)
                return Response(supplier_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Daha önce herhangi bir tedarikçi oluşturulmadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
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


class SupplierUpdateAPIView(UpdateAPIView):
    serializer_class = SupplierSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put',)
    schema = CreateSupplierSchema
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Supplier.objects.all()


class SupplierDeleteAPIView(DestroyAPIView):
    serializer_class = SupplierSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Supplier.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": _("Tedarikçi bilgileri başarıyla kaldırıldı.")}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": _("Tedarikçi bilgileri bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def list_product_order_view(request):
    """
    API endpoint that return product order information
    """
    if request.method == "GET":
        try:
            product_order = ProductOrder.objects.all().order_by('-created_at')
            if product_order.count() != 0:
                product_order_serializer = ProductOrderSerializer(product_order, many=True)
                return Response(product_order_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Daha önce herhangi bir ürün siparişi oluşturulmadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateProductOrderSchema, )
def create_product_order_view(request):  # Testing doesnt not yet.
    """
    API endpoint that create product order
    """
    try:
        client = Client.objects.get(email=request.data["client"])
        product_order = ProductOrder(client=client, name=request.data["name"], quantity=request.data["quantity"])
        product_order.save()
        return Response({"detail": _("Ürün siparişi başarı ile oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ProductOrderUpdateAPIView(UpdateAPIView):
    serializer_class = ProductOrderSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put',)
    schema = CreateProductOrderSchema
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = ProductOrder.objects.all()


class ProductOrderDeleteAPIView(DestroyAPIView):
    serializer_class = ProductOrderSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = ProductOrder.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": _("Ürün siparişi bilgileri başarıyla kaldırıldı.")}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": _("Ürün siparişi bilgileri bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def list_raw_order_view(request):
    """
    API endpoint that return raw order information
    """
    if request.method == "GET":
        try:
            raw_order = RawOrder.objects.all().order_by('-created_at')
            if raw_order.count() != 0:
                raw_order_serializer = RawOrderSerializer(raw_order, many=True)
                return Response(raw_order_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Daha önce herhangi bir malzeme siparişi oluşturulmadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateRawOrderSchema, )
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


class RawOrderUpdateAPIView(UpdateAPIView):
    serializer_class = RawOrderSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put',)
    schema = CreateRawOrderSchema
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = RawOrder.objects.all()


class RawOrderDeleteAPIView(DestroyAPIView):
    serializer_class = RawOrderSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = RawOrder.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": _("Ham madde siparişi bilgileri başarıyla kaldırıldı.")},
                            status=status.HTTP_200_OK)
        except:
            return Response({"detail": _("Ham madde siparişi bilgileri bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def budget_total_view(request):
    """
    API endpoint that return total money on system
    """
    if request.method == "GET":
        try:
            budget = Budget.objects.all().order_by('-created_at')
            if budget.count() != 0:
                budget_serializer = BudgetSerializer(budget, many=True)
                return Response(budget_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Bütçe bilgisi bulunamadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def budget_income_detail_and_total_view(request):
    """
    API endpoint that return total income money on system
    """
    if request.method == "GET":  # Total money recevier should be appended to model
        try:
            budget = Budget.objects.exclude(product_order__isnull=True).order_by('-created_at')
            if budget.count() != 0:
                budget_serializer = BudgetSerializer(budget, many=True)
                return Response(budget_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Bütçe bilgisi bulunamadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def budget_outcome_detail_and_total_view(request):
    """
    API endpoint that return total outcome money on system
    """
    if request.method == "GET":  # Total money recevier should be appended to model
        try:
            budget = Budget.objects.exclude(raw_order__isnull=True).order_by('-created_at')
            if budget.count() != 0:
                budget_serializer = BudgetSerializer(budget, many=True)
                return Response(budget_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Bütçe bilgisi bulunamadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
