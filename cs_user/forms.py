# -* - coding: utf-8 -*-
import logging

from django import forms
from django.forms import ModelForm
from django.forms.widgets import Textarea

from cs_user.models import User


class UserCreateForm(ModelForm):

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

class UserUpdateForm(UserCreateForm):
    
    class Meta(UserCreateForm.Meta):
        pass 


class EmployeeUpdateForm(ModelForm):
    
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions',
                   'is_staff', 'is_active', 'date_joined', 'company', 'company_name', 'address',
                   'city', 'postcode', 'secondary_phone', 'subscriber', 'role', 'username')

