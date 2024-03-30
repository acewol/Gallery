from django.urls import re_path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', mainapp.index, name='index'),
    re_path(r'^contact/$', mainapp.contact, name='contact'),
    re_path(r'^products/$', mainapp.products, name='products'),
    re_path(r'^products/category/(?P<category_pk>\d+)/$', mainapp.products, name='category'),
    re_path(r'^product/(?P<product_pk>\d+)/$', mainapp.product, name='product'),
]
