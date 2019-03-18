from django.urls import path, include
from api.v1.views import *


urlpatterns = [
    path('user/', hello, name='hello'),
    path('register/', register_view),
]
