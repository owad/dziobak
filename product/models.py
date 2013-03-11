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

    key = models.IntegerField(verbose_name=u'numer zgłoszenia')
    
    class Meta(ABM.Meta):
        verbose_name_plural = u'zgłoszenia'
        verbose_name = u'zgłoszenie'
        ordering = ['-modified']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk, 'user_pk': self.user.pk})

    def save(self):
        last = Product.objects.filter(user__company=self.user.company, created__year=datetime.now().year).order_by('-pk')
        key = 1
        if last:
            key = last[0].key + 1

        self.key = key
        return super(Product, self).save()
   
    def __unicode__(self):
        return "%s/%s" % (self.created.year, str(self.key).zfill(4))

class Comment(ABM):

    # Statuses
    STATUS = {10: 'przyjęty',
              20: 'w realizacji',
              30: 'do wydania',
              40: 'wydany'}

    ORDERED_STATUS_CHOICES =[(key, STATUS[key]) for key in STATUS.keys()]

    description = models.TextField(default='-', verbose_name='komentarz')
    product = models.ForeignKey('Product')
    user = models.ForeignKey(User)  # employee (determines who is an owner of a product)
    status = models.CharField(max_length=64, choices=ORDERED_STATUS_CHOICES, verbose_name='status')

    class Meta(ABM.Meta):
        verbose_name_plural = "komentarze"
        verbose_name = "komentarz"
        ordering = ['-created']

    def __unicode__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.product.pk, 'user_pk': self.product.user.pk})

