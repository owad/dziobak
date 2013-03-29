from django import forms
from django.forms import ModelForm

from product.models import Product, Comment, Courier
from product.constants import STATUSES


class ProductCreateForm(ModelForm):

    class Meta:
        model = Product
        exclude = ('user', 'company', 'modified', 'status', 'key')


class ProductUpdateForm(ProductCreateForm):
    pass


class CommentCreateForm(ModelForm):

    status = forms.ChoiceField(choices=STATUSES)

    class Meta:
        model = Comment
        exclude = ('user', 'modified', 'product')
    
