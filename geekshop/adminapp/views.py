from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from authapp.models import ShopUser
from django.contrib.auth.decorators import user_passes_test
from mainapp.models import Product, ProductCategory
from adminapp.forms import ShopUserRegisterAdminForm, ShopUserEditAdminForm, CategoryEditAdminForm, ProductEditAdminForm, ProductAuctionEditAdminForm


@user_passes_test(lambda x: x.is_superuser)
def index(request):
    title = 'Админка | Пользователи'
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list,
    }

    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_create(request):
    title = 'Пользователи | Создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterAdminForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:index'))
    else:
        user_form = ShopUserRegisterAdminForm()
    
    context = {
        'title': title,
        'form': user_form,
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_update(request, user_pk):
    title = 'Пользователи | Редактирование'
    user = get_object_or_404(ShopUser, pk=user_pk)

    if request.method == 'POST':
        user_form = ShopUserEditAdminForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:index'))
    else:
        user_form = ShopUserEditAdminForm(instance=user)
    
    context = {
        'title': title,
        'form': user_form,
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def categories(request):
    title = 'Админка | Категории'
    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list,
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_create(request):
    title = 'Категории | Создание'

    if request.method == 'POST':
        category_form = CategoryEditAdminForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = CategoryEditAdminForm()
    
    context = {
        'title': title,
        'form': category_form,
    }

    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_update(request, category_pk):
    title = 'Категории | Редактирование'
    category = get_object_or_404(ProductCategory, pk=category_pk)

    if request.method == 'POST':
        category_form = CategoryEditAdminForm(request.POST, request.FILES, instance=category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = CategoryEditAdminForm(instance=category)
    
    context = {
        'title': title,
        'form': category_form,
    }

    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def products(request, category_pk):
    title = 'Админка | Продукты'
    products_list = Product.objects.filter(category__pk=category_pk).order_by('name')

    context = {
        'title': title,
        'objects': products_list,
        'category_pk': category_pk,
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_create(request):
    title = 'Продукты | Создание'

    if request.method == 'POST':
        product_form = ProductEditAdminForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        product_form = ProductEditAdminForm()
    
    context = {
        'title': title,
        'form': product_form,
    }

    return render(request, 'adminapp/product_create.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_update(request, product_pk):
    title = 'Продукты | Редактирование'
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == 'POST':
        product_form = ProductEditAdminForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        product_form = ProductEditAdminForm(instance=product)
    
    context = {
        'title': title,
        'form': product_form,
    }

    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_update_auction(request, product_pk):
    title = 'Аукцион | Редактирование'
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == 'POST':
        product_form = ProductAuctionEditAdminForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        product_form = ProductAuctionEditAdminForm(instance=product)

    context = {
        'title': title,
        'form': product_form,
    }

    return render(request, 'adminapp/product_update_auction.html', context)