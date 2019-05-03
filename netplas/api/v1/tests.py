from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from product.models import Product, Raw
from product.serializers import ProductSerializer, RawSerializer
from stock.models import ProductStock, RawStock

from profile.models import UserProfile


class Test(APITestCase):

    def setUp(self):
        self.raw_stock = RawStock.objects.create(name='TestRawStock')
        self.product_stock = ProductStock.objects.create(name='TestProductStock')
        self.product = Product.objects.create(stock=self.product_stock, name='TestProduct', quantity=10)
        self.raw = Raw.objects.create(stock=self.raw_stock, name='TestRaw', quantity=10)
        self.user = UserProfile.objects.create(email='utkucanbykl@test.com')

    def test_update_raw(self):
        client = APIClient()
        url = reverse_lazy('api:raw-update', kwargs={'id': self.raw.id})
        update_data = {
            'name': 'TestUpdateRaw'
        }
        token = Token.objects.get(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.patch(url, update_data)
        print(response.data)
        self.assertEqual(response.data['name'], 'TestUpdateRaw')

    def test_update_product(self):
        client = APIClient()
        url = reverse_lazy('api:product-update', kwargs={'id': self.product.id})
        update_data = {
            'name': 'TestUpdateProduct'
        }
        token = Token.objects.get(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.patch(url, update_data)
        print(response.data)
        self.assertEqual(response.data['name'], 'TestUpdateProduct')
