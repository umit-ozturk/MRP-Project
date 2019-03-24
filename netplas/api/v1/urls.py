from django.urls import path, include
from api.v1.views import *


urlpatterns = [
    path('user/', hello, name='hello'),
    path('register/', register_view),
    path('login/', login_view),
    path('product_stock/list', list_product_stock),
    path('raw_stock/list', list_raw_stock),
]
