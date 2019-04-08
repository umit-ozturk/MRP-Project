from django.urls import path, include
from api.v1.views import *

app_name = 'api'

urlpatterns = [
    path('test/', test_view, name='test_service'),
    path('register/', register_view, name='register_service'),
    path('login/', login_view, name='login_service'),

    path('product_stock/list', list_product_stock_view, name='product_stock_list_service'),
    path('product_stock/create', create_product_stock_view, name='product_stock_create_service'),
    path('product_stock/update/<int:id>/', ProductStockUpdateAPIView.as_view(), name='product_stock_update_service'),

    path('product/list', list_product_info_view, name='product_list_service'),
    path('product/create', create_product_view, name='product_create_service'),
    path('product/update/<int:id>/', ProductUpdateAPIView.as_view(), name='product_update_service'),

    path('raw_stock/list', list_raw_stock_view, name='raw_stock_list_service'),
    path('raw_stock/create', create_raw_stock_view, name='raw_stock_create_service'),
    path('raw_stock/update/<int:id>/', RawStockUpdateAPIView.as_view(), name='raw_stock_update-service'),

    path('raw/list', list_raw_info_view, name='raw_list_service'),
    path('raw/create', create_raw_view, name='raw_create_service'),
    path('raw/update/<int:id>/', RawUpdateAPIView.as_view(), name='raw_update_service'),

    path('client/list', list_client_view, name='client_list_service'),
    path('client/create', create_client_view, name='client_create_service'),
    path('client/update/<int:id>/', ClientUpdateAPIView.as_view(), name='client-update-service'),

    path('supplier/list', list_supplier_view, name='supplier_list_service'),
    path('supplier/create', create_supplier_view, name='supplier_create_service'),
    path('supplier/update/<int:id>/', SupplierUpdateAPIView.as_view(), name='supplier-update-service'),

    path('product_order/list', list_product_order_view, name='product_order_list_service'),
    path('product_order/create', create_product_order_view, name='product_order_create_service'),
    path('product_order/update/<int:id>/', ProductOrderUpdateAPIView.as_view(), name='product-order-update-service'),

    path('raw_order/list', list_raw_order_view, name='raw_order_list_service'),
    path('raw_order/create', create_raw_order_view, name='raw_order_create_service'),
    path('raw_order/update/<int:id>/', RawOrderUpdateAPIView.as_view(), name='raw-order-update-service'),

]
