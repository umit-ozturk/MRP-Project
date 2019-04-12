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
    path('product_stock/delete/<int:id>/', ProductStockDeleteAPIView.as_view(), name='product_stock_delete_service'),

    path('product/list', list_product_info_view, name='product_list_service'),
    path('product/create', create_product_view, name='product_create_service'),
    path('product/update/<int:id>/', ProductUpdateAPIView.as_view(), name='product_update_service'),
    path('product/delete/<int:id>/', ProductDeleteAPIView.as_view(), name='product_delete_service'),

    path('raw_stock/list', list_raw_stock_view, name='raw_stock_list_service'),
    path('raw_stock/create', create_raw_stock_view, name='raw_stock_create_service'),
    path('raw_stock/update/<int:id>/', RawStockUpdateAPIView.as_view(), name='raw_stock_update_service'),
    path('raw_stock/delete/<int:id>/', RawStockDeleteAPIView.as_view(), name='raw_stock_delete_service'),

    path('raw/list', list_raw_info_view, name='raw_list_service'),
    path('raw/create', create_raw_view, name='raw_create_service'),
    path('raw/update/<int:id>/', RawUpdateAPIView.as_view(), name='raw_update_service'),
    path('raw/delete/<int:id>/', RawDeleteAPIView.as_view(), name='raw_delete_service'),

    path('client/list', list_client_view, name='client_list_service'),
    path('client/create', create_client_view, name='client_create_service'),
    path('client/update/<int:id>/', ClientUpdateAPIView.as_view(), name='client_update_service'),
    path('client/delete/<int:id>/', ClientDeleteAPIView.as_view(), name='client_delete_service'),

    path('supplier/list', list_supplier_view, name='supplier_list_service'),
    path('supplier/create', create_supplier_view, name='supplier_create_service'),
    path('supplier/update/<int:id>/', SupplierUpdateAPIView.as_view(), name='supplier_update_service'),
    path('supplier/delete/<int:id>/', SupplierDeleteAPIView.as_view(), name='supplier_delete_service'),

    path('product_order/list', list_product_order_view, name='product_order_list_service'),
    path('product_order/create', create_product_order_view, name='product_order_create_service'),
    path('product_order/update/<int:id>/', ProductOrderUpdateAPIView.as_view(), name='product_order_update_service'),
    path('product_order/delete/<int:id>/', ProductOrderDeleteAPIView.as_view(), name='product_order_delete_service'),

    path('raw_order/list', list_raw_order_view, name='raw_order_list_service'),
    path('raw_order/create', create_raw_order_view, name='raw_order_create_service'),
    path('raw_order/update/<int:id>/', RawOrderUpdateAPIView.as_view(), name='raw_order_update_service'),
    path('raw_order/delete/<int:id>/', RawOrderDeleteAPIView.as_view(), name='raw_order_delete_service'),

    path('budget/total/', budget_total_view, name='total_budget_service'),
    path('budget/total/income/', budget_income_detail_and_total_view, name='income_detail_and_total_budget_service'),

]
