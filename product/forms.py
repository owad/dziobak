from django import forms
from django.forms import ModelForm

from product.models import Product, Comment, Courier


class ProductCreateForm(ModelForm):

    class Meta:
        model = Product
        exclude = ('user', 'modified')


class ProductUpdateForm(ProductCreateForm):
    pass


class CommentCreateForm(ModelForm):

    class Meta:
        model = Comment
        
