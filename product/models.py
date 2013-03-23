# -* - coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db import models
from django.db.models import Manager, Q
from django.core.urlresolvers import reverse

from product.constants import *
from cs_user.models import User, Company
from base.models import AbstractBaseModel as ABM
from base.utils import get_company


class Courier(ABM):
    
    name = models.CharField(max_length='64')
    
    class Meta(ABM.Meta):
        verbose_name_plural = "kurierzy"
        verbose_name = "kurier"
    
    def __unicode__(self):
        return self.name


class ProductManager(Manager):

    def search(self, qs, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).filter(
            Q(name__icontains=qs) |
            Q(producent__icontains=qs) |
            Q(serial__icontains=qs) |
            Q(invoice__icontains=qs) |
            Q(key__icontains=qs))        

    def get_query_set(self):
        company = get_company()
        queryset = super(ProductManager, self).get_query_set()
        if company:
            return queryset.filter(company=company)
        return queryset


class Product(ABM):

    name = models.CharField(max_length=128, verbose_name='nazwa')
    producent = models.CharField(max_length=128, blank=True, verbose_name='producent')
    serial = models.CharField(max_length=128, blank=True, verbose_name='numer seryjny')
    invoice = models.CharField(max_length=128, blank=True, verbose_name='numer faktury')
    description = models.TextField(verbose_name='opis usterki')
    warranty = models.CharField(max_length=8, default='nie', choices=[('nie', 'Nie'), ('tak', 'Tak')], verbose_name='gwarancja')
    status = models.CharField(max_length=64, verbose_name='status')
    user = models.ForeignKey(User)  # client (not an emplyee)
    company = models.ForeignKey(Company)

    key = models.IntegerField(verbose_name=u'numer zgłoszenia')

    objects = ProductManager()
    
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
    
    def get_details_list(self):
        fields = ['name', 'producent', 'serial', 'invoice', 'description', 'waranty', 'status']
        data = []

        data.append(('klient', self.user.get_full_name()))

        for field in fields:
            value = getattr(self, field, None)
            if value:
                data.append((self._meta.get_field(field).verbose_name, value))
        return data

    @property
    def cost(self):
        return sum([sum(c) for c in self.comment_set.all().values_list('cost_service', 'cost_hardware', 'cost_transport')])        

    @property
    def serviced_by(self):
        employee = Comment.objects.filter(product=self, status=Comment.S20)
        if employee:
            return employee[0].user
        return '-'

    def get_status(self):
        return dict(Comment.STATUSES)[self.status]

    def get_name(self):
        return ', '.join(set([self.name, self.producent]))

    @property
    def last_comment(self):
        return Comment.objects.filter(product=self).order_by('-pk')[0]

class Comment(ABM):

    # Statuses
    S10 = 10
    S20 = 20
    S30 = 30
    S40 = 40
    
    STATUSES = [(S10, 'przyjęty'),
              (S20, 'w realizacji'),
              (S30, 'do wydania'),
              (S40, 'wydany')]

    STATUS_KEYS = [key for key, name in STATUSES]

    description = models.TextField(verbose_name='komentarz')
    product = models.ForeignKey('Product')
    user = models.ForeignKey(User)  # employee (determines who is an owner of a product)
    status = models.IntegerField(choices=STATUSES, verbose_name='status')

    cost_service = models.FloatField(default=0.0, verbose_name='koszt usługi')
    cost_hardware = models.FloatField(default=0.0, verbose_name='koszt sprzętu')
    cost_transport = models.FloatField(default=0.0, verbose_name='koszt dojazdu')

    class Meta(ABM.Meta):
        verbose_name_plural = "komentarze"
        verbose_name = "komentarz"
        ordering = ['created']

    def __unicode__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.product.pk, 'user_pk': self.product.user.pk})

    def get_status(self):
        return dict(Comment.STATUSES)[self.status]

    @property
    def cost(self):
        return self.cost_service + self.cost_hardware + self.cost_transport

