from django.urls import path, include
from api.v1.views import *

app_name = 'api'

urlpatterns = [
    path('test/', test_view, name='test_service'),
    path('register/', register_view, name='register_service'),
    path('login/', login_view, name='login_service'),
    path('product_stock/list', list_product_stock_view, name='product_stock_list_service'),
    path('product_stock/create', create_product_stock_view, name='create_product_stock_service'),
    path('product/list', list_product_info_view, name='product_info_by_name_service'),
    path('product/create', create_product_view, name='create_product_service'),
    path('raw_stock/list', list_raw_stock_view, name='raw_stock_list_service'),
    path('raw_stock/create', create_raw_stock_view, name='create_raw_stock_service'),
    path('raw/list', list_raw_info_view, name='raw_info_by_name_service'),
    path('raw/create', create_raw_view, name='create_raw_service'),
    path('raw/update/<int:id>/', RawUpdateAPIView.as_view(), name='raw-update'),

]
