from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from cs import settings

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'product.views.product_list', name='home'),

    url(r'^zaloguj/$', login, {'template_name': 'registration/login.html'}, name='cs_login'),
    url(r'^wyloguj/$', logout, {'template_name': 'registration/logout.html'}, name='cs_logout'),

    # clients
    url(r'^klient/', include('cs_user.urls')),

    # employees
    url(r'^pracownik/zmien_haslo$', 'user_password_change', name='user_password_reset'),

    # products
    url(r'^zgloszenie/', include('product.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

