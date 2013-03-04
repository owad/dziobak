from django import forms
from django.forms import ModelForm

from cs_user.models import User

class UserCreateForm(ModelForm):

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'is_active', 'date_joined', 'company')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].widget.attrs['readonly'] = True

class UserUpdateForm(UserCreateForm):
    pass   
 
