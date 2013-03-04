from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class UserRequiredMiddleware(object):
    """ Middleware that only allows whitelisted users to view the site whilst it's in development. """

    def process_request(self, request):
        
        current_url = request.get_full_path().split('?')[0]
        
        if not request.user.is_authenticated() and current_url not in (reverse('cs_login'), reverse('cs_logout')):
            return redirect('%s?next=%s' % (reverse('cs_login'), request.path))
        return None

