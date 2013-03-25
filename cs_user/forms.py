from django import forms
from django.forms import ModelForm
from django.forms.widgets import Textarea

from cs_user.models import User


class UserCreateForm(ModelForm):

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions',
                   'is_staff', 'is_active', 'date_joined', 'company')

    address = forms.CharField(widget=Textarea)    
    role = forms.ChoiceField(choices=User.CLIENTS, initial=User.CLIENT)   
 
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].widget.attrs['readonly'] = True


class UserUpdateForm(UserCreateForm):
    
    class Meta(UserCreateForm.Meta):
        exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 
                   'is_staff', 'is_active', 'date_joined', 'company', 'role', 'company_name',
                   'subscriber')
       


class EmployeeUpdateForm(ModelForm):
    
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions',
                   'is_staff', 'is_active', 'date_joined', 'company', 'company_name', 'address',
                   'city', 'postcode', 'secondary_phone', 'subscriber', 'role', 'username')

