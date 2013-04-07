from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
import logging


class UserRequiredMiddleware(object):
    """ Middleware that only allows whitelisted users to view the site whilst it's in development. """

    def process_request(self, request):
        
        current_url = request.get_full_path().split('?')[0]

        user = request.user
        if user and user.is_authenticated() and not user.company.active:
            messages.add_message(request, messages.SUCCESS, 'Konto nie aktywne')
            #return redirect(reverse('cs_logout'))
            

        # check if user allowed to see content 
        if not request.user.is_authenticated() and current_url not in (reverse('cs_login'), reverse('cs_logout')):
            return redirect('%s?next=%s' % (reverse('cs_login'), request.path))
      
        # put company object into a session 
        if request.user.is_authenticated():
            request.session['company'] = request.user.company
        else:
            request.session['company'] = None
        return None

