import logging

from django import forms
from django.forms import ModelForm

from product.models import Product, Comment, Courier


class ProductForm(ModelForm):

    class Meta:
        model = Product
        exclude = ('user', 'company', 'modified', 'status', 'key')


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'modified', 'product', 'status', 'status_changed')


class ClientCommentForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'modified', 'product', 'status', 'cost_service', 'cost_hardware', 'cost_transport')

