from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse


urlpatterns = patterns('cs_user.views',

    url(r'^klienci/lista$', 'user_list', name='user_list'),
    url(r'^klient/(?P<pk>\d+)/szczegoly$', 'user_detail', name='user_detail'),
    url(r'^klient/nowy$', 'user_create', name='user_create'),
    url(r'^klient/edytuj/(?P<pk>\d+)$', 'user_update', name='user_update'),

    # employees
    url(r'^profil/edytuj$', 'profile_update', name='profile_update'),

    # employers and superusers only
    url(r'^pracownicy$', 'employee_list', name='employee_list'),
    url(r'^pracownik/nowy$', 'employee_create', name='employee_create'),
    url(r'^pracownik/edytuj/(?P<pk>\d+)$', 'employee_update', name='employee_update'),

    # company
    url(r'^firma/edytuj/(?P<pk>\d+)$', 'company_update', name='company_update'),
)

