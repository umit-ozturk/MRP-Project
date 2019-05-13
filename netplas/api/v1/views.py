from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, schema, authentication_classes
from rest_framework.generics import UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.views import APIView
from django.db.models import F
from rest_framework import status
from api.v1.schemas import RegisterSchema, LoginSchema, RawInfoSchema, ProductInfoSchema, CreateProductStockSchema, \
    CreateRawStockSchema, CreateProductSchema, CreateRawSchema, CreateClientSchema, CreateSupplierSchema, \
    CreateProductOrderSchema, CreateRawOrderSchema, DamagedCreateRawOrderSchema, DamagedCreateProductOrderSchema, \
    CreateProductTemplateSchema, UpdatePassword, UpdateProductSchema, UpdateRawSchema, NotAuthenticatedUpdatePassword, UpdateProductStockSchema
from api.v1.tools import create_profile, check_user_is_valid
from profile.serializers import UserProfileSerializer, UserProfileUpdateSerializer
from stock.serializers import ProductStockSerializer, RawStockSerializer
from product.serializers import ProductSerializer, RawSerializer, \
    RawForProdSerializer, ProductUpdateSerializer, RawForProdUpdateSerializer, RawUpdateSerializer
from system.serializers import DamagedProductSerializer, DamagedRawSerializer
from stock.models import ProductStock, RawStock
from product.models import Product, Raw, RawForProduction, ProductAttr
from system.models import Client, Supplier, ProductOrder, RawOrder, Budget, DamagedProduct, DamagedRaw
from system.serializers import ClientSerializer, SupplierSerializer, ProductOrderSerializer, RawOrderSerializer, \
    BudgetSerializer, BudgetTotalSerializer, ClientUpdateSerializer, SupplierUpdateSerializer
from profile.models import UserProfile
from decimal import Decimal


@api_view(['POST'])
@schema(RegisterSchema, )
def register_view(request):
    """
    API endpoint that allows users to register.
    """
    try:
        request.POST._mutable = True
        create_profile(request.user, request.data)
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
            product_stock_serializer = ProductStockSerializer(product_stock, many=True)
            return Response(product_stock_serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": _("Daha önce herhangi bir ürün deposu oluşturulmadı.")},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateProductStockSchema, )
def create_product_stock_view(request):
    """
    API endpoint that create product stock
    """
    try:
        raw_stock, created = ProductStock.objects.get_or_create(name=request.data['product_stock_name'])
        if not created:
            return Response({"detail": _("Ürün deposu zaten mevcut.")}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"detail": _("Ürün deposu başarıyla oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ProductStockUpdateAPIView(UpdateAPIView):
    serializer_class = ProductStockSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch',)
    schema = UpdateProductStockSchema
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
        except Exception as ex:
            print(str(ex))
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
        raw_stock, created = RawStock.objects.get_or_create(name=request.data['raw_stock_name'])
        if not created:
            return Response({"detail": _("Ham madde deposu zaten mevcut.")}, status=status.HTTP_200_OK)
        return Response({"detail": _("Ham madde deposu başarıyla oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class RawStockUpdateAPIView(UpdateAPIView):
    serializer_class = RawStockSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch',)
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
        except Exception as ex:
            print(str(ex))
            return Response({"detail": _("Ham madde deposu bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def list_all_product_info_view(request):
    """
    API endpoint that return all product and quantity
    """
    if request.method == "GET":
        try:
            product_info = Product.objects.all().order_by('-created_at')
            product_info_serializer = ProductSerializer(product_info, many=True)
            return Response(product_info_serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": _("Kayıtlı bir ürün bilgisi bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


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
                print(product_info)
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
        product_stock = ProductStock.objects.get(name=request.data["product_stock_name"])
        product = Product(stock=product_stock, name=request.data["product_name"],
                          unit_price=request.data["unit_price"], amount=request.data['amount'])
        product.save()
        for attr in request.data.get('product_attr', []):
            ProductAttr.objects.create(**attr, product=product)
        return Response({"detail": _("Ürün başarıyla oluşturuldu.")},
                        status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"detail": _("Ürün deposu bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        print(str(ex))
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateAPIView(UpdateAPIView):
    serializer_class = ProductUpdateSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch',)
    schema = UpdateProductSchema
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Product.objects.all()

    def update(self, request, *args, **kwargs):
        if request.data.get('product_stock_name'):
            stock_name = request.data.pop('product_stock_name')
            stock_id = ProductStock.objects.filter(name=stock_name).first().id
            request.data.update({'stock': stock_id})
        return super().update(request, *args, **kwargs)

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
        except Exception as ex:
            print(str(ex))
            return Response({"detail": _("Ürün bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


class RawForProductListAPIView(ListAPIView):
    serializer_class = RawForProdSerializer
    queryset = RawForProduction.objects.filter()
    
    def get_queryset(self):
        qs = super(RawForProductListAPIView, self).get_queryset()
        if self.request.GET.get('product_name', None):
            return qs.filter(product__name=self.request.GET.get('product_name')).order_by('-created_at')
        return qs


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateProductTemplateSchema, )
def create_product_template_view(request):
    """
    API endpoint that create product template
    """
    try:
        quantity = request.data['quantity']
        if int(quantity) > 0:
            raw = Raw.objects.get(name=request.data["raw_name"])
            product = Product.objects.get(name=request.data['product_name'])
            raw_for_product = RawForProduction(raw=raw, product=product, quantity_for_prod=int(quantity))
            raw_for_product.save()
            return Response({"detail": _(str(quantity) + " adet ürün başarıyla oluşturuldu.")},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": _("Ürün miktarını doğru giriniz.")}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"detail": _("Ürün deposu bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ProductTemplateUpdateAPIView(UpdateAPIView):
    serializer_class = RawForProdUpdateSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch',)
    schema = CreateProductTemplateSchema
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = RawForProduction.objects.all()

    def update(self, request, *args, **kwargs):
        if request.data.get('raw_name'):
            raw_name = request.data.pop('raw_name')
            raw = Raw.objects.filter(name=raw_name).first().id
            request.data.update(
                {'raw': raw}
            )
        if request.data.get('product_name'):
            product_name = request.data.pop('product_name')
            product = Product.objects.filter(name=product_name).first().id
            request.data.update(
                {'product': product}
            )
        return super().update(request, *args, **kwargs)



class ProductTemplateDeleteAPIView(DestroyAPIView):
    serializer_class = RawForProdSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = RawForProduction.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": _("Ürün ham madde gereklilik şeması başarıyla kaldırıldı.")},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": _("Ürün ham madde gereklilik şeması bulunamadı.")},
                            status=status.HTTP_404_NOT_FOUND)


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


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def list_all_raw_info_view(request):
    """
    API endpoint that return all raw list
    """
    if request.method == "GET":
        try:
            raw_info = Raw.objects.all().order_by('-created_at')
            raw_info_serializer = RawSerializer(raw_info, many=True)
            return Response(raw_info_serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": _("Ham madde bilgisi bulunamadı.")}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(CreateRawSchema, )
def create_raw_view(request):
    """
    API endpoint that create raw
    """
    try:
        param = request.data
        raw_stock = RawStock.objects.get(name=param["raw_stock_name"])
        raw = Raw(stock=raw_stock, name=param["raw_name"], amount=param["amount"],
                  unit_price=param["unit_price"])
        raw.save()
        return Response({"detail": _("Ham madde başarıyla oluşturuldu.")},
                        status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"detail": _("Ham madde deposu bulunamadı.")}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class RawUpdateAPIView(UpdateAPIView):
    serializer_class = RawUpdateSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch',)
    schema = UpdateRawSchema
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = Raw.objects.all()

    def update(self, request, *args, **kwargs):
        if request.data.get('raw_stock_name'):
            raw_name = request.data.pop('raw_stock_name')
            raw = RawStock.objects.filter(name=raw_name).first().id
            request.data.update(
                {'stock': raw}
            )
        return super().update(request, *args, **kwargs)

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
        except Exception as ex:
            print(str(ex))
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
                        phone=request.data["phone"], address=request.data['address'], company=request.data['company'])
        client.save()
        return Response({"detail": _("Müşteri başarı ile oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ClientUpdateAPIView(UpdateAPIView):
    serializer_class = ClientUpdateSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch',)
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
        except Exception as ex:
            print(str(ex))
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
    serializer_class = SupplierUpdateSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch',)
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
        except Exception as ex:
            print(str(ex))
            return Response({"detail": _("Tedarikçi bilgileri bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def list_product_order_view(request):
    """
    API endpoint that return product order information
    """
    if request.method == "GET":
        try:
            product_order = ProductOrder.objects.filter().select_related('product', 'client', 'personal').order_by()
            if product_order.exists():
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
        client = Client.objects.get(email=request.data["client_email"])
        personal = UserProfile.objects.get(email=request.data['user_email'])
        product = Product.objects.filter(name=request.data["product_name"]).first()
        if request.data['status']:
            product_order = ProductOrder(client=client, product=product, quantity=Decimal(request.data["quantity"]),
                                         personal=personal, order_title=request.data['order_title'],
                                         status=request.data['status'])
        else:
            product_order = ProductOrder(client=client, product=product, quantity=Decimal(request.data["quantity"]),
                                         personal=personal, order_title=request.data['order_title'])
        product_order.save()
        return Response({"detail": _("Ürün siparişi başarı ile oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        print(str(ex))
        return Response({"detail": _("Girilen bilgiler yanlış veya depoda yeterli hammadde yok.")},
                        status=status.HTTP_400_BAD_REQUEST)


class ProductOrderUpdateAPIView(UpdateAPIView):
    serializer_class = ProductOrderSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch',)
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
        except Exception as ex:
            print(str(ex))
            return Response({"detail": _("Ürün siparişi bilgileri bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def list_raw_order_view(request):
    """
    API endpoint that return raw order information
    """
    if request.method == "GET":
        try:
            raw_order = RawOrder.objects.filter().select_related('supplier', 'personal', 'raw').order_by('-created_at')
            if raw_order.exists():
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
def create_raw_order_view(request):  # Testing doesnt not yet.
    """
    API endpoint that create raw order
    """
    try:
        supplier = Supplier.objects.get(email=request.data["supplier_email"])
        personal = UserProfile.objects.get(email=request.data['user_email'])
        raw = Raw.objects.filter(name=request.data["raw_name"]).first()
        if request.data['status']:
            raw_order = RawOrder(supplier=supplier, raw=raw, quantity=Decimal(request.data["quantity"]),
                                 personal=personal, order_title=request.data['order_title'],
                                 status=request.data['status'])
        else:
            raw_order = RawOrder(supplier=supplier, product=raw, quantity=Decimal(request.data["quantity"]),
                                 personal=personal, order_title=request.data['order_title'])
        raw_order.save()
        return Response({"detail": _("Tedarikçi başarı ile oluşturuldu.")}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"detail": _("Girilen bilgiler yanlış veya hammadde tanımlanmamış.")},
                        status=status.HTTP_400_BAD_REQUEST)


class RawOrderUpdateAPIView(UpdateAPIView):
    serializer_class = RawOrderSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch',)
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
        except Exception as ex:
            print(str(ex))
            return Response({"detail": _("Ham madde siparişi bilgileri bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@schema(RawInfoSchema, )
def list_damaged_raw_info_view(request):
    """
    API endpoint that return damaged raw and quantity by damaged raw name
    """
    if request.method == "GET":
        try:
            raw = Raw.objects.get(name=request.data["raw_name"])
            damaged_raw_info = DamagedRaw.objects.filter(raw=raw).order_by('-created_at')
            if damaged_raw_info.count() != 0:
                damaged_raw_info_serializer = DamagedRaw(damaged_raw_info, many=True)
                return Response(damaged_raw_info_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Ham madde bilgisi bulunamadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(DamagedCreateRawOrderSchema, )
def create_damaged_raw_view(request):
    """
    API endpoint that create damaged raw
    """
    try:
        raw = Raw.objects.get(name=request.data["raw_name"])
        damaged_raw = DamagedRaw(raw=raw)
        damaged_raw.save()
        return Response({"detail": _(" adet hasarlı ham madde başarıyla oluşturuldu.")}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"detail": _("Hasarlı ham madde deposu bulunamadı.")}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class DamagedRawUpdateAPIView(UpdateAPIView):
    serializer_class = DamagedRawSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch',)
    schema = DamagedCreateRawOrderSchema
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = DamagedRaw.objects.all()


class DamagedRawDeleteAPIView(DestroyAPIView):
    serializer_class = DamagedRawSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = DamagedRaw.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": _("Hasarlı Ham madde başarıyla kaldırıldı.")}, status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": _("Hasarlı Ham madde bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@schema(ProductInfoSchema, )
def list_damaged_product_info_view(request):
    """
    API endpoint that return damaged product and quantity by damaged product name
    """
    if request.method == "GET":
        try:
            product = Product.objects.get(name=request.data["product_name"])
            damaged_product_info = DamagedProduct.objects.filter(product=product).order_by('-created_at')
            if damaged_product_info.count() != 0:
                damaged_product_info_serializer = DamagedProduct(damaged_product_info, many=True)
                return Response(damaged_product_info_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Hasarlı ürün bilgisi bulunamadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@schema(DamagedCreateProductOrderSchema, )
def create_damaged_product_view(request):
    """
    API endpoint that create damaged product
    """
    try:
        product = Product.objects.get(name=request.data["product_name"])
        damaged_product = DamagedProduct(product=product)
        damaged_product.save()
        return Response({"detail": _(" adet hasarlı ürün başarıyla oluşturuldu.")}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"detail": _("Hasarlı product deposu bulunamadı.")}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class DamagedProductUpdateAPIView(UpdateAPIView):
    serializer_class = DamagedProductSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ('put', 'patch',)
    schema = DamagedCreateProductOrderSchema
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = DamagedProduct.objects.all()


class DamagedProductDeleteAPIView(DestroyAPIView):
    serializer_class = DamagedProductSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = DamagedProduct.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": _("Hasarlı ürün başarıyla kaldırıldı.")}, status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": _("Hasarlı ürün bulunamadı.")}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def budget_total_view(request):
    """
    API endpoint that return total money on system
    """
    if request.method == "GET":
        budget = Budget.objects.filter()
        try:
            if budget.exists():
                budget = budget.first()
                budget_serializer = BudgetTotalSerializer(budget, many=False)
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
    if request.method == "GET":  # Total money receiver should be appended to model
        try:
            budget = Budget.objects.exclude(product_order__isnull=True).order_by('-created_at')
            if budget.exists():
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
    if request.method == "GET":  # Total money receiver should be appended to model
        try:
            budget = Budget.objects.exclude(raw_order__isnull=True).order_by('-created_at')
            if budget.exists():
                budget_serializer = BudgetSerializer(budget, many=True)
                return Response(budget_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": _("Bütçe bilgisi bulunamadı.")},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ControlSecretAnswer(UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    http_method_names = ['put', ]
    schema = UpdatePassword

    def get_queryset(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.secret_answer == request.data['secret_answer']:
            user.set_password(request.data['new_password'])
            user.save()
            return Response({'success': 'Parola Başarıyla Değiştirildi'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Gizli Soru Cevabı Hatalı'}, status=status.HTTP_403_FORBIDDEN)


class NotAuthenticatedControlSecretAnswer(UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    http_method_names = ['put', 'patch']
    schema = NotAuthenticatedUpdatePassword

    def get_queryset(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(email=request.data['email'])
            if user.secret_answer == request.data['secret_answer'] and request.data['new_password'] == \
                    request.data['new_password_again']:
                user.set_password(request.data['new_password'])
                user.save()
                return Response({'success': _('Parola Başarıyla Değiştirildi')}, status=status.HTTP_201_CREATED)
            return Response({'error': _('Gizli Soru Cevabı Hatalı')}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({'error': _('Personel bilgisi bulunamadı')}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def get_all_user(request):
    """
    API endpoint that return all users
    """
    if request.method == "GET":
        try:
            users = UserProfile.objects.filter()
            serialized_users = UserProfileSerializer(users, many=True)
            return Response(serialized_users.data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(str(ex))
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
