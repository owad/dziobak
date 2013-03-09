from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse


urlpatterns = patterns('cs_user.views',
    url(r'^$', 'user_list', name='user_list'),
    url(r'^(?P<pk>\d+)$', 'user_detail', name='user_detail'),
    url(r'^utworz$', 'user_create', name='user_create'),
    url(r'^edytuj/(?P<pk>\d+)$', 'user_update', name='user_update'),
    url(r'^zmien_haslo$', 'user_password_change', name='user_password_reset'),

)

