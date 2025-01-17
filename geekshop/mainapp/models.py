from django.db import models
from django.utils import timezone
from authapp.models import ShopUser


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='наименование категории', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание категории', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='название картины', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_description = models.CharField(verbose_name='краткое описание картины', max_length=60, blank=True)
    full_description = models.TextField(verbose_name='описание картины', blank=True)
    price = models.DecimalField(verbose_name='цена картины', max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(verbose_name='количество в галереи', default=0)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    auction_last_user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, null=True, blank=True)

    auction = models.BooleanField(verbose_name='Выставлен на аукцион', default=False)
    auction_time_start = models.DateTimeField(verbose_name='Время начала аукциона', default=timezone.now)
    auction_time_end = models.DateTimeField(verbose_name='Время окончания аукциона', default=timezone.now)
    auction_bet = models.PositiveIntegerField(verbose_name='Минимальная ставка', default=1000)
    auction_current_cost = models.PositiveIntegerField(verbose_name='Текущая ставка', default=1000)


    def __str__(self):
        return f'{self.name} ({self.category.name})'
