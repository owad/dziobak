from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

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
    context_object_name = 'users'
    queryset = User.objects.all()
    paginate_by = ROWS_PER_PAGE

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

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])

user_update = UserUpdate.as_view()

