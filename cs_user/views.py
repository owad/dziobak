from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator

from cs.settings import ROWS_PER_PAGE
from cs_user.models import User
from cs_user.forms import UserCreateForm, UserUpdateForm


class UserDetail(DetailView):
    context_object_name = 'client'
    model = User
    '''
    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company)
    '''
user_detail = UserDetail.as_view()


class UserList(ListView):
    context_object_name = 'clients'
    paginate_by = ROWS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        if q:
            return User.objects.search(q)
        return User.objects.all()

user_list = UserList.as_view()
    

class UserCreate(CreateView):
    form_class = UserCreateForm
    template_name = 'cs_user/user_create_or_update.html'

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super(UserCreate, self).form_valid(form)

user_create = UserCreate.as_view()


class UserUpdate(UpdateView):
    form_class = UserUpdateForm
    template_name = 'cs_user/user_create_or_update.html'
    context_object_name = 'client'

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])

user_update = UserUpdate.as_view()


def user_password_reset(request):

    template_name='registration/password_reset_form.html'
    post_reset_redirect = reverse('user_detail', kwargs={'pk': request.user.pk})

    return password_reset(request,
                   template_name=template_name,
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=post_reset_redirect)

