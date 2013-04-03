# -* - coding: utf-8 -*-
import logging
from datetime import datetime, timedelta

from django.db import models
from django.db.models import Manager, Q
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save

from product.constants import *
from cs_user.models import User, Company
from base.models import AbstractBaseModel as ABM
from base.utils import get_company, get_user


class Courier(ABM):
    
    name = models.CharField(max_length='64')
    
    class Meta(ABM.Meta):
        verbose_name_plural = "kurierzy"
        verbose_name = "kurier"
    
    def __unicode__(self):
        return self.name


class ProductManager(Manager):

    def search(self, qs, *args, **kwargs):
        return self.get_query_set(*args, **kwargs).filter(
            Q(name__icontains=qs) |
            Q(producent__icontains=qs) |
            Q(serial__icontains=qs) |
            Q(invoice__icontains=qs) |
            Q(key__icontains=qs))        

    def get_query_set(self):
        user = get_user()
        queryset = super(ProductManager, self).get_query_set()
        if user:
            if user.is_client_with_access:
                return queryset.filter(company=user.company, user=user)
            if user.is_employee:
                company = user.company
                return queryset.filter(company=company)
        return queryset


class Product(ABM):

    name = models.CharField(max_length=128, verbose_name='nazwa')
    producent = models.CharField(max_length=128, blank=True, verbose_name='producent')
    serial = models.CharField(max_length=128, blank=True, verbose_name='numer seryjny')
    invoice = models.CharField(max_length=128, blank=True, verbose_name='numer faktury')
    description = models.TextField(verbose_name='opis usterki')
    warranty = models.CharField(max_length=8, default='nie', choices=[('nie', 'Nie'), ('tak', 'Tak')], verbose_name='gwarancja')
    status = models.IntegerField(verbose_name='status', default=NEW)
    max_cost = models.FloatField(default=0.0, verbose_name='maksymalny koszt naprawy')

    user = models.ForeignKey(User)  # client (not an emplyee)
    company = models.ForeignKey(Company)

    key = models.IntegerField(verbose_name=u'numer zgłoszenia', default=0)

    objects = ProductManager()
    
    class Meta(ABM.Meta):
        verbose_name_plural = u'zgłoszenia'
        verbose_name = u'zgłoszenie'
        ordering = ['-modified']

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk, 'user_pk': self.user.pk})

    def __unicode__(self):
        return "%s/%s" % (self.created.year, str(self.key).zfill(4))

    def save(self):
        try:
            self.status = self.comment_set.latest('pk').status
        except Comment.DoesNotExist:
            pass
        return super(Product, self).save()        

    @property
    def statuses(self):
        if self.user.is_normal_client:
            return C1_STATUSES
        if self.user.is_client_with_access:
            return C2_STATUSES

    @property
    def status_names(self):
        if self.user.is_normal_client:
            return C1_STATUS_NAMES
        if self.user.is_client_with_access:
            return C2_STATUS_NAMES
        
    @property
    def status_flow(self):
        if self.user.is_normal_client:
            return C1_STATUSES_FLOW
        if self.user.is_client_with_access:
            return C2_STATUSES_FLOW

    @property
    def init_status(self):
        if self.user.is_normal_client:
            return NEW
        if self.user.is_client_with_access:
            return REG

    @property
    def can_update_status(self):
        if self.is_employee:
            return True
        if self.is_client_with_access and self.status in (TO_APPR,):
            return True
        return False

    @property
    def cost(self):
        return sum([sum(c) for c in self.comment_set.all().values_list('cost_service', 'cost_hardware', 'cost_transport')])        

    @property
    def cost_desc(self):
        costs = [0.0, 0.0, 0.0]
        names = ['usługa', 'sprzęt', 'transport']
        result = self.comment_set.all().values_list('cost_service', 'cost_hardware', 'cost_transport')
        for s, h, t in result:
            costs[0] += s
            costs[1] += h
            costs[2] += t

        return ', '.join([ "%s: %szł" % (names[key], value) for key, value in enumerate(costs) if value > 0])

    def get_user_by_comment_status(self, status):
        employee = Comment.objects.filter(product=self, status=status)
        if employee:
            return employee[0].user
        return None

    @property
    def added_by(self):
        return self.get_user_by_comment_status(NEW)
    
    @property
    def serviced_by(self):
        return self.get_user_by_comment_status(PROG)

    @property
    def fixed_by(self):
        return self.get_user_by_comment_status(READY)

    @property
    def get_status(self):
        try:
            return STATUS_NAMES[self.status]
        except KeyError:
            return STATUS_NAMES[NEW]

    @property
    def get_name(self):
        if self.producent:
            return ', '.join([self.name, self.producent])
        return self.name

    @property
    def last_comment(self):
        return Comment.objects.filter(product=self).order_by('-pk')[0]

    def next_status_choices(self):
        ''' return a list of tuples used as forms choices '''
        try:
            keys = self.status_flow[self.status]
        except KeyError:
            keys = self.status_flow[self.init_status]
        choices = []
        for k in keys:
            choices.append((k, STATUS_NAMES[k]))
        return choices


class Comment(ABM):

    description = models.TextField(verbose_name='komentarz')
    product = models.ForeignKey('Product')
    user = models.ForeignKey(User)  # employee (determines who is an owner of a product)
    status = models.IntegerField(verbose_name='status')
    attachment = models.FileField(upload_to='data/attachments', null=True, blank=True)

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
        return STATUS_NAMES[self.status]

    @property
    def cost(self):
        return self.cost_service + self.cost_hardware + self.cost_transport


def update_key(instance, **kwargs):
    if not instance.pk:
        last = Product.objects.filter(created__year=datetime.now().year).order_by('-pk')
        try:
            key = last[0].key
            instance.key = key + 1
        except IndexError:
            instance.key = 1

pre_save.connect(update_key, sender=Product)

