# -* - coding: utf-8 -*-
import logging

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages

from cs.settings import ROWS_PER_PAGE
from cs_user.models import User
from cs_user.forms import UserForm, EmployeeForm, EmployerForm


class UserDetail(DetailView):
    context_object_name = 'client'
    model = User

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
        queryset = User.objects.filter(role__in=User.CLIENT_KEYS)
        if q:
            return queryset.search(q)
        return queryset

user_list = UserList.as_view()

    
class EmployeeList(UserList):
    context_object_name = 'employees'
    template_name = 'cs_user/employee_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.all_objects.filter(role__in=User.EMPLOYEE_KEYS)
        return User.objects.filter(role__in=User.EMPLOYEE_KEYS)
         

employee_list = EmployeeList.as_view()


class UserCreate(CreateView):
    form_class = UserForm
    template_name = 'cs_user/user_create_or_update.html'

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        messages.add_message(self.request, messages.SUCCESS, 'Klient został dodany')
        return super(UserCreate, self).form_valid(form)

user_create = UserCreate.as_view()


class EmployeeCreate(UserCreate):
    template_name = 'cs_user/employee_create_or_update.html'
    form_class = EmployeeForm

    def get_form(self, form_class):
        self.form_class = EmployeeForm
        if self.request.user.is_superuser:
            self.form_class = EmployerForm
        return  super(EmployeeCreate, self).get_form(self.form_class)

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        form.instance.role = User.EMPLOYEE
        messages.add_message(self.request, messages.SUCCESS, 'Pracownik został dodany')
        return super(UserCreate, self).form_valid(form)
    
employee_create = EmployeeCreate.as_view()


class UserUpdate(UpdateView):
    form_class = UserForm
    template_name = 'cs_user/user_create_or_update.html'
    context_object_name = 'client'

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Dane Klienta zostały zaktualizowanne')
        return super(UserUpdate, self).get_success_url()

user_update = UserUpdate.as_view()


class ProfileUpdate(UserUpdate):
    form_class = EmployeeForm
    template_name = 'cs_user/profile_update.html'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        new_password = self.request.POST.get('password1', None)
        result = super(ProfileUpdate, self).form_valid(form)

        if new_password:
            user = self.get_object()
            user.set_password(new_password)
            user.save()
            messages.add_message(self.request, messages.SUCCESS, 'Hasło zostało zmienione')

        return result

profile_update = ProfileUpdate.as_view()


class EmployeeUpdate(ProfileUpdate):
    template_name = 'cs_user/employee_create_or_update.html'

    def get_form(self, form_class):
        self.form_class = EmployeeForm
        if self.request.user.is_superuser:
            self.form_class = EmployerForm
        return  super(EmployeeUpdate, self).get_form(self.form_class)

    def get_object(self):
        if self.request.user.is_superuser:
            return User.all_objects.get(pk=self.kwargs['pk']) 
        return User.objects.get(company=self.request.user.company, pk=self.kwargs['pk']) 
        
    def get_success_url(self):
        return reverse('employee_list')

employee_update = EmployeeUpdate.as_view()


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

