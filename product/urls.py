from django.conf.urls import patterns, include, url


urlpatterns = patterns('product.views',

    # products
    url(r'^lista$', 'product_list', name='product_list'),
    url(r'^(?P<pk>\d+)/klient/(?P<user_pk>\d+)$', 'product_detail', name='product_detail'),
    url(r'^(?P<pk>\d+)/klient/(?P<user_pk>\d+)/pdf$', 'product_pdf', name='product_pdf'),
    url(r'^nowe/(?P<user_pk>\d+)', 'product_create', name='product_create'),
    url(r'^edytuj/(?P<pk>\d+)/klient/(?P<user_pk>\d+)$', 'product_update', name='product_update'),

    # comments
    url(r'^(?P<product_pk>\d+)/komentarz/nowy', 'comment_create', name='comment_create'),
)
