from django.conf.urls import patterns, include, url


urlpatterns = patterns('product.views',

    # products
    url(r'^$', 'product_list', name='product_list'),
    url(r'^(?P<pk>\d+)$', 'product_detail', name='product_detail'),
    url(r'^utworz/(?P<user_pk>\d+)', 'product_create', name='product_create'),
    url(r'^edytuj/(?P<pk>\d+)$', 'product_update', name='product_update'),

    # comments
    url(r'^komenatrz/utworz/(?P<product_pk>\d+)', 'comment_create', name='comment_create'),

)

