from django.db import models
from django.conf import settings
from mainapp.models import Product
from authapp.models import ShopUser
""""
 sum колличества товаров
 sum итоговой стоимости товаров
"""
class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = self.user.basket_set.all()
        return sum(list(map(lambda x: x.quantity, _items)))
    
    @property
    def total_cost(self):
        _items = self.user.basket_set.all()
        return sum(list(map(lambda x: x.product_cost, _items)))

class Cart(models.Model):
    userid = models.ForeignKey(ShopUser, on_delete=models.PROTECT, related_name='userid')
    product = models.ManyToManyField(Product, related_name='product')
    quantity = models.DecimalField(verbose_name='Количество', max_digits=8, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(verbose_name='Общая стоимость', max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return self.userid