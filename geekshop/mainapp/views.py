from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from mainapp.models import Product, ProductCategory


MENU_ITEMS = {
    'index': 'Главная',
    'products': 'Продукция',
    'contact': 'Контакты',
}


def get_basket(request):
    return request.user.basket_set.all() if request.user.is_authenticated else []


def index(request):
    context = {
        'title': 'главная',
        'menu': MENU_ITEMS,
        'basket': get_basket(request),
    }

    send_mail(
        subject="ведите свой заголовок сюда",
        message="твою мать ебали волки",
        from_email='mypraktik1@gmail.com',
        recipient_list=['yarikbocc2015@gmail.com']
    )
    
    return render(request, 'mainapp/index.html', context)


def products(request, category_pk=None):
    title = 'продукция'
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    context = {
        'title': title,
        'menu': MENU_ITEMS,
        'products': products,
        'categories': categories,
        'basket': get_basket(request),
    }

    if category_pk:
        if category_pk == '0':
            category = {'name': 'все'}
            products = Product.objects.all().order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=category_pk)
            products = Product.objects.filter(category__pk=category_pk).order_by('price')

        context['products'] = products
        context['category'] = category

    return render(request, 'mainapp/products.html', context)


def product(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    context = {
        'title': product.name,
        'menu': MENU_ITEMS,
        'product': product,
        'basket': get_basket(request),
    }

    return render(request, 'mainapp/product.html', context)


def contact(request):
    contacts = {
        'address': {
            'key': 'Адрес',
            'val': 'Москва, ул. Барклая, 11',
        },
        'phone': {
            'key': 'Телефон',
            'val': '8 (495) 123-45-67'
        },
        'mail': {
            'key': 'Почта',
            'val': 'egallery@mail.egallery.ru',
        },
        'shipping': {
            'key': 'Доставка',
            'val': 'Все города России',
        },
    }

    context = {
        'title': 'контакты',
        'menu': MENU_ITEMS,
        'contacts': contacts,
        'basket': get_basket(request),
    }
    
    return render(request, 'mainapp/contact.html', context)
