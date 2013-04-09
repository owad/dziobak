from django.conf.urls import patterns, include, url

urlpatterns = patterns('product.views',

    # products
    url(r'^lista$', 'product_list', name='product_list'),
    url(r'^lista/(?P<status>\d+)/$', 'product_list',  name='product_list'),

    url(r'^klient/(?P<user_pk>\d+)/zgloszenie/(?P<pk>\d+)/szczegoly$', 'product_detail', name='product_detail'),
    url(r'^klient/(?P<user_pk>\d+)/zgloszenie/(?P<pk>\d+)/pdf$', 'product_pdf', name='product_pdf'),
    url(r'^klient/(?P<user_pk>\d+)/zgloszenie/nowe$', 'product_create', name='product_create'),
    url(r'^klient/(?P<user_pk>\d+)/zgloszenie//(?P<pk>\d+)/edytuj/$', 'product_update', name='product_update'),

    # comments
    url(r'^zgloszneie/(?P<product_pk>\d+)/komentarz/nowy', 'comment_create', name='comment_create'),

    # files
    url(r'^zgloszneie/(?P<product_pk>\d+)/komentarz/(?P<pk>\d+)/zalacznik', 'serve_attachment', name='serve_attachment'),
    url(r'^logo', 'serve_logo', name='serve_logo'),
)

