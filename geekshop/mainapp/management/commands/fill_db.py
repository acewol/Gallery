from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser

import json
import os

JSON_PATH = os.path.join('mainapp', 'json')

def get_data_from_json(file_name):
    with open(os.path.join(JSON_PATH, f'{file_name}.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):
    help = 'Fill database with data'

    def handle(self, *args, **options):
        categories = get_data_from_json('categories')
        ProductCategory.objects.all().delete()
        categories_objs = []
        for category in categories:
            categories_objs.append(ProductCategory(**category))
        ProductCategory.objects.bulk_create(categories_objs)

        products = get_data_from_json('products')
        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            _category = ProductCategory.objects.filter(name=category_name).first()
            product['category'] = _category
            Product(**product).save()

        _superuser = ShopUser.objects.filter(username='django').first()
        if not _superuser:
            ShopUser.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', age=29)
            print('Created super user django')