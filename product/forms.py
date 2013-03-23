from django import forms
from django.forms import ModelForm

from product.models import Product, Comment, Courier


class ProductCreateForm(ModelForm):

    class Meta:
        model = Product
        exclude = ('user', 'company', 'modified', 'status', 'key')


class ProductUpdateForm(ProductCreateForm):
    pass


class CommentCreateForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'modified', 'product')
    
