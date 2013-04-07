import logging

from django.core.urlresolvers import resolve
from django.http import Http404

from cs_user.models import User
from product.models import Product


ACCESS_LIST = {
    User.CLIENT_WITH_ACCESS: {'allowed': ['user_detail', 'product_create', 'product_detail', 'comment_create', 'serve_attachment', 'serve_logo']},
    User.EMPLOYEE: {'forbidden': ['employee_list', 'employee_create', 'employee_update', 'company_update', 'company_create']},
    User.EMPLOYER: {}
}


def d(msg):
    pass#logging.warning(msg)

def no_access():
    raise Http404()


class UserCheckAccess(object):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        company = request.session.get('company', None)
        d('User role = %s' % user.role)        
        product = self.get_product()
        client = self.get_client()

        # check if user belongs to a company
        if user.company != company:
            logging.warning('Company access not allowed')
            no_access()
        d('1'*10)
        # client with access checks
        if user.is_client_with_access:
            if self.url_name not in ACCESS_LIST[user.role]['allowed']:
                logging.warning('Client with access has no access to "%s" view' % self.url_name)
                no_access()
            d('2'*10)
           
            if client and client != user:
                logging.warning('Client with access can access only his own user data')
                no_access()
        
            d('3'*10)

            if product and product.user != user:
                logging.warning('Client with access can access only his own products data')
                no_access()

        d('4'*10)

        # employees checks 
        if user.role == User.EMPLOYEE:
            if self.url_name in ACCESS_LIST[user.role]['forbidden']:
                logging.warning('Employee has not access to "%s" view' % self.url_name)
                no_access()
        d('5'*10)

        return super(UserCheckAccess, self).dispatch(request, *args, **kwargs)

    def get_client(self):
        if 'pk' in self.kwargs.keys():
            try:
                return User.objects.get(pk=self.kwargs['pk'])
            except User.DoesNotExist:
                pass
        return None

    def get_product(self):
        if 'pk' in self.kwargs.keys():
            try:
                return Product.objects.get(pk=self.kwargs['pk'])
            except Product.DoesNotExist:
                pass
        return None
        
    @property
    def url_name(self):
        return resolve(self.request.path).url_name

