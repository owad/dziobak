# -* - coding: utf-8 -*-
import logging

from django import forms
from django.forms import ModelForm
from django.forms.widgets import Textarea

from cs_user.models import User


class UserForm(ModelForm):

    class Meta:
        model = User
        exclude = ('username', 'password', 'last_login', 'is_superuser', 'groups', 'user_permissions',
                   'is_staff', 'is_active', 'date_joined', 'company')

    address = forms.CharField(widget=Textarea)    
    role = forms.ChoiceField(choices=User.CLIENTS, initial=User.CLIENT)   
 
    def clean(self):
        if not (self.cleaned_data['first_name'].strip() and self.cleaned_data['last_name'].strip()) and not self.cleaned_data['company_name'].strip():
            raise forms.ValidationError('Podaj imię i nazwisko klienta lub nazwę firmy')

        return self.cleaned_data


class EmployeeForm(ModelForm):

    password1 = forms.CharField(max_length=30, widget=forms.widgets.PasswordInput(), label="Hasło", required=False)
    password2 = forms.CharField(max_length=30, widget=forms.widgets.PasswordInput(), label="Powtórz hasło", required=False)

    first_name = forms.CharField(max_length=64, label="Imię", required=True)
    last_name = forms.CharField(max_length=64, label="Nazwisko", required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions',
                   'is_staff', 'is_active', 'date_joined', 'company', 'company_name', 'address',
                   'city', 'postcode', 'secondary_phone', 'subscriber', 'role')

    def clean(self):
        password1 = self.data.get('password1')
        password2 = self.data.get('password2')

        if (password1 or password2) and password1 != password2:
            raise forms.ValidationError("Hasła nie zgadzają się")

        if not self.instance.pk:
            if not password1:
                raise forms.ValidationError("Hasło jest wymagane")

        return self.cleaned_data


    def clean_username(self):
        username = self.cleaned_data.get('username')
        queryset = User.all_objects.filter(username=username)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.count() > 0:
            raise forms.ValidationError("Nazwa użytkownika niedostępna")
        return username


class EmployerForm(EmployeeForm):

    class Meta(EmployeeForm.Meta):
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions',
                   'is_staff', 'is_active', 'date_joined', 'company_name', 'address',
                   'city', 'postcode', 'secondary_phone', 'subscriber', 'role')

