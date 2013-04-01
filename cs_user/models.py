# -* - coding: utf-8 -*-
import re
import logging

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict
from django.template.defaultfilters import slugify

from base.models import AbstractBaseModel as ABM
from base.utils import get_company

from product.constants import *


class Company(ABM):

    class Meta(ABM.Meta):
        verbose_name = "firma"
        verbose_name_plural = "firmy"
    
    name = models.CharField(max_length=128)
    logo = models.FileField(upload_to="media/logo", blank=True)

    domain = models.CharField(max_length=128, verbose_name="domena", blank=True)
    slug = models.SlugField(max_length=128, blank=True)

    active = models.BooleanField(default=True, verbose_name="firma aktywna")

    def __unicode__(self):
        return self.name

    @property
    def statuses(self):
        return STATUSES


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Company, self).save(*args, **kwargs)


class UserManager(DjangoUserManager):

    def create_superuser(self, username, email, password, **extra_fields):
        user = super(UserManager, self).create_superuser(username, email, password, **extra_fields)
        user.company, _ = Company.objects.get_or_create(name='Admins')
        user.role = User.EMPLOYER
        user.save()
        return user

    def search(self, qs, *args, **kwargs):
        return self.get_query_set(*args, **kwargs).filter(
            Q(first_name__icontains=qs) |
            Q(last_name__icontains=qs) |
            Q(company_name__icontains=qs) |
            Q(city__icontains=qs) |
            Q(postcode__icontains=qs) |
            Q(primary_phone__icontains=qs))        


    def get_query_set(self):
        company = get_company()
        queryset = super(UserManager, self).get_query_set()
        if company:
            return queryset.filter(company=company)
        return queryset


class User(AbstractUser):

    EMPLOYER = 9
    EMPLOYEE = 10
    CLIENT_WITH_ACCESS = 20
    CLIENT = 30

    ROLE_CHOICES = [
        (EMPLOYEE, 'Serwisant'),
        (CLIENT_WITH_ACCESS, 'Klient z dostępem do zleceń'),
        (CLIENT, 'Zwykły klient')]

    CLIENTS = [
        (CLIENT_WITH_ACCESS, 'Klient z dostępem do zleceń'),
        (CLIENT, 'Zwykły klient')]

    EMPLOYEES = [
        (EMPLOYER, 'pracodawca'),
        (EMPLOYEE, 'pracownik'),
    ]

    CLIENT_KEYS = [CLIENT_WITH_ACCESS, CLIENT]
    EMPLOYEE_KEYS = [EMPLOYEE, EMPLOYER]

    objects = UserManager()

    class Meta:
        verbose_name = "użytkownik"
        verbose_name_plural = "użytkownicy"

    role = models.IntegerField(default=CLIENT, choices=ROLE_CHOICES, verbose_name="typ")
    company = models.ForeignKey('Company', null=True)  # only for users with role EMPLOYEE
    
    company_name = models.CharField(max_length=128, blank=True, verbose_name='firma')
    address = models.CharField(max_length=128, blank=True, verbose_name='adres')
    city = models.CharField(max_length=128, blank=True, verbose_name='miejscowość')
    postcode = models.CharField(max_length=8, blank=True, verbose_name='kod pocztowy')

    primary_phone = models.CharField(max_length=9, validators=[RegexValidator('^(\d{9})$')], verbose_name='telefon')
    secondary_phone = models.CharField(max_length=9, validators=[RegexValidator('^(\d{9})$')], blank=True, verbose_name='telefon dodatkowy')

    subscriber = models.BooleanField(default=False, verbose_name='abonament serwisowy')

    def __unicode__(self):
        if self.role == User.EMPLOYEE:
            data = [self.get_full_name(), self.company.name]
        else:
            data = [self.get_full_name(), self.company_name]

        return ', '.join(data).strip(', ')

    def get_absolute_url(self):
        if self.role in User.CLIENT_KEYS:
            return reverse('user_detail', kwargs={'pk': self.pk})
        else:
            return reverse('employee_update', kwargs={'pk': self.pk})

    @property
    def is_employee(self):
        return self.role in User.EMPLOYEE_KEYS
    
    @property
    def is_client(self):
        return not self.is_employee

    @property
    def phone_numbers(self):
        if self.secondary_phone:
            return "%s, %s" % (self.primary_phone, self.secondary_phone)
        return self.primary_phone


    def save(self, *args, **kwargs):
        if self.company_name:
            username = self.company_name
        else:
            username = self.get_full_name()

        '''
        if not self.pk:
            self.username = re.sub(r'\W+', '', username).lower()
        '''

        return super(User, self).save(*args, **kwargs)

