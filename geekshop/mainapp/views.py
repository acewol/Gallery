import datetime
from django.utils import timezone


from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from mainapp.models import Product, ProductCategory
from mainapp.forms import ProductAuctionEditForm

MENU_ITEMS = {
    'index': 'Главная',
    'products': 'Продукция',
    'contact': 'Контакты',
    'auction': 'Аукцион',
}


def check_final_auction(request, current_product):
    if timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone()) > current_product.auction_time_end:
        msg = f"Добрый день!\n" \
              f"Вы победили на аукционе!!\n" \
              f"Название товара - {current_product.name}\n" \
              f"В итоге вы должны заплатить - {current_product.auction_current_cost}\n"

        send_mail(
            subject="И У НАС ПОБЕДИТЕЛЬ!!!",
            message=msg,
            from_email='mypraktik1@gmail.com',
            recipient_list=['yarikbocc2015@gmail.com']
        )

        current_product.auction_last_user = None
        current_product.auction = False
        current_product.auction_time_start = datetime.datetime.now()
        current_product.auction_time_end   = datetime.datetime.now()
        current_product.auction_bet        = 1000
        current_product.auction_current_cost = 1000
        current_product.save()

        return True
    return False


def get_basket(request):
    return request.user.basket_set.all() if request.user.is_authenticated else []


def index(request):
    context = {
        'title': 'главная',
        'menu': MENU_ITEMS,
        'basket': get_basket(request),
    }
    #
    # send_mail(
    #     subject="ведите свой заголовок сюда",
    #     message="твою мать ебали волки",
    #     from_email='mypraktik1@gmail.com',
    #     recipient_list=['yarikbocc2015@gmail.com']
    # )
    
    return render(request, 'mainapp/index.html', context)


def products(request, category_pk=None):
    title = 'Продукция'
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


def auction(request, category_pk=None):
    title = 'Аукцион'
    auction_products = Product.objects.filter(auction=True)
    categories = ProductCategory.objects.all()
    context = {
        'title': title,
        'menu': MENU_ITEMS,
        'products': auction_products,
        'categories': categories,
        'basket': get_basket(request),
    }

    if category_pk:
        if category_pk == '0':
            category = {'name': 'все'}
            auction_products = Product.objects.filter(auction=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=category_pk)
            auction_products = Product.objects.filter(auction=True, category__pk=category_pk).order_by('price')

        context['products'] = auction_products
        context['category'] = category

    return render(request, 'mainapp/auction.html', context)


def product(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if check_final_auction(request, product):
        return HttpResponseRedirect(reverse('mainapp:auction'))
    context = {
        'title': product.name,
        'menu': MENU_ITEMS,
        'product': product,
        'basket': get_basket(request),
    }

    return render(request, 'mainapp/product.html', context)


def auction_product(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    error = ''
    if check_final_auction(request, product):
        return HttpResponseRedirect(reverse('mainapp:auction'))


    if request.method == 'POST' and 'bet' in request.POST:
        bet = int(request.POST['bet'])
        if bet >= product.auction_bet:
            product.auction_current_cost += bet
            product.auction_last_user_id = request.user
            product.save()
        else:
            error = f'Ставка должна быть больше {product.auction_bet}'
        # if product_form.is_valid():
        #     product_form.save()
        #     return HttpResponseRedirect(reverse('mainapp:auction'))

    context = {
        'title': product.name,
        'menu': MENU_ITEMS,
        'product': product,
        'basket': get_basket(request),
        'error': error,

    }

    return render(request, 'mainapp/auction_product.html', context)


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

# форинг кей для продукта на юзера для аукциона
# при заходе на страницу товара, чек на тайм, убирать его из актива и аннулировать все аукционные поля
# slam.medvedi@gmail.com
#