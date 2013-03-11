# -* - coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db import models
from django.db.models import Sum, Count
from django.core.urlresolvers import reverse

from product.constants import *
from cs_user.models import User
from base.models import AbstractBaseModel as ABM


class Courier(ABM):
    
    name = models.CharField(max_length='64')
    
    class Meta(ABM.Meta):
        verbose_name_plural = "kurierzy"
        verbose_name = "kurier"
    
    def __unicode__(self):
        return self.name


class Product(ABM):

    name = models.CharField(max_length=128, verbose_name='nazwa')
    producent = models.CharField(max_length=128, blank=True, verbose_name='producent')
    serial = models.CharField(max_length=128, blank=True, verbose_name='numer seryjny')
    invoice = models.CharField(max_length=128, blank=True, verbose_name='numer faktury')
    description = models.TextField(verbose_name='opis usterki')
    warranty = models.CharField(max_length=8, default='nie', choices=[('nie', 'Nie'), ('tak', 'Tak')], verbose_name='gwarancja')
    status = models.CharField(max_length=64, verbose_name='status')
    user = models.ForeignKey(User)  # client (not an emplyee)
    
    
    class Meta(ABM.Meta):
        verbose_name_plural = "zgłoszenia"
        verbose_name = "zgłoszenie"
        ordering = ['-modified']

    def __unicode__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


class Comment(ABM):

    # Statuses
    S10 = (10, 'przyjęty')
    S20 = (20, 'w realizacji')
    S30 = (30, 'do wydania')
    S40 = (40, 'wydany')

    description = models.TextField(default='-', verbose_name='komentarz')
    product = models.ForeignKey('Product')
    user = models.ForeignKey(User)  # employee (determines who is an owner of a product)
    status = models.CharField(max_length=64, choices=[S10, S20, S30, S40], verbose_name='status')

    class Meta(ABM.Meta):
        verbose_name_plural = "komentarze"
        verbose_name = "komentarz"
        ordering = ['-created']

    def __unicode__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.product.pk})

