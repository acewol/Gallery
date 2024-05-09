from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from basketapp.models import Basket, Cart
from django.views.generic import TemplateView
from mainapp.models import Product
from mainapp.views import get_basket



# @login_required
# def index(request):
#     basket_items = request.user.basket_set.all()
#     context = {
#         'title': 'корзина',
#         'basket_items': basket_items,
#     }
#
#     return render(request, 'basketapp/basket.html', context)



class Index(TemplateView):
    template_name = "basketapp/basket.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        basket_items = self.request.user.basket_set.all()

        context['title'] = 'корзина'
        context['basket_items'] = basket_items

        return context

    def post(self, request, *args, **kwargs):
        for key in request.POST.items():
            if key[0].startswith('111'):
                quantity = key[0][3:]
                price = key[1][3:]

        product_list = request.user.basket_set.all()
        userid = request.user

        print(f"quantity - {quantity}")
        print(f"price - {price}")
        print(f"product_list - {product_list}")
        print(f"userid - {userid}")

        new_basket_item = Cart.objects.create(userid=request.user, price=price, quantity=quantity)
        for i in range(product_list.count()):
            new_basket_item.product.add(product_list[i].product)

        new_basket_item.save()
        # MAIL PUSH
        return super(Index, self).get(request, *args, **kwargs)

@login_required
def add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:product', kwargs={
            'product_pk': pk,
        }))
    
    product = get_object_or_404(Product, pk=pk)
    old_basket_item = Basket.objects.filter(user=request.user, product=product)

    if old_basket_item:
        old_basket_item[0].quantity += 1
        old_basket_item[0].save()
    else:
        new_basket_item = Basket(user=request.user, product=product, quantity=1)
        new_basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    get_object_or_404(Basket, pk=pk, user=request.user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def update(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.filter(pk=int(pk)).first()

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()
        
        basket_items = request.user.basket_set.all()

        context = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc__basket_list.html', context)

        return JsonResponse({
            'result': result,
        })

