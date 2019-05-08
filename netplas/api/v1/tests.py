from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from product.models import Product, Raw
from product.serializers import ProductSerializer, RawSerializer
from stock.models import ProductStock, RawStock
from django.contrib.auth.hashers import make_password

from profile.models import UserProfile


class Test(APITestCase):

    def setUp(self):
        self.user = UserProfile.objects.create(email='utkucanbykl@test.com', secret_answer='1')
        self.user.set_password('123')
        self.user.save()


    def test_update_user(self):
        client = APIClient()
        url = reverse_lazy('api:update-password')
        token = Token.objects.get(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'new_password': '123456',
            'secret_answer': '1'
        } 
        response = client.put(url, data)
        user = UserProfile.objects.get(email='utkucanbykl@test.com')
        self.assertTrue(user.check_password('123456'))
