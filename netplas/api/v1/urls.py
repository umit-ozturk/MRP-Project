from django.urls import path, include
from api.v1.views import hello


urlpatterns = [
    path('user/', hello, name='hello'),
]
