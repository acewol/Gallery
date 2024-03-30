from django.urls import re_path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    re_path(r'^$', adminapp.index, name='index'),
    re_path(r'^user/create/$', adminapp.user_create, name='user_create'),
    re_path(r'^user/update/(?P<user_pk>\d+)$', adminapp.user_update, name='user_update'),
    re_path(r'^categories/$', adminapp.categories, name='categories'),
    re_path(r'^categories/create/$', adminapp.category_create, name='category_create'),
    re_path(r'^categories/update/(?P<category_pk>\d+)$', adminapp.category_update, name='category_update'),
    re_path(r'^products/(?P<category_pk>\d+)/$', adminapp.products, name='products'),
    re_path(r'^products/create/$', adminapp.product_create, name='product_create'),
    re_path(r'^products/update/(?P<product_pk>\d+)$', adminapp.product_update, name='product_update'),
]