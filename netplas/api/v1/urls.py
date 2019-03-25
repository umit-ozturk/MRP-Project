from django.urls import path, include
from api.v1.views import *


urlpatterns = [
    path('test/', test_view, name='test_service'),
    path('register/', register_view, name='register_service'),
    path('login/', login_view, name='login_service'),
    path('product_stock/list', list_product_stock_view, name='product_stock_list_service'),
    path('product_info/list', list_product_info_view, name='product_info_by_name_service'),
    path('raw_stock/list', list_raw_stock_view, name='raw_stock_list_service'),
    path('raw_info/list', list_raw_info_view, name='raw_info_vy_name_service'),
]
