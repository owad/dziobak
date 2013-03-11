# -* - coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict

from base.models import AbstractBaseModel as ABM


class Company(ABM):

    class Meta(ABM.Meta):
        verbose_name = "firma"
        verbose_name_plural = "firmy"
    
    name = models.CharField(max_length=128)
    logo = models.FileField(upload_to="media/logo", blank=True)

    def __unicode__(self):
        return self.name


class UserManager(DjangoUserManager):

    def create_superuser(self, username, email, password, **extra_fields):
        user = super(UserManager, self).create_superuser(username, email, password, **extra_fields)
        user.company, _ = Company.objects.get_or_create(name='Admins')
        user.save()
        return user


class User(AbstractUser):

    EMPLOYEE = 10
    CLIENT_WITH_ACCESS = 20
    CLIENT = 30

    ROLE_CHOICES = [
        (EMPLOYEE, 'Serwisant'),
        (CLIENT_WITH_ACCESS, 'Klient z dostępem do zleceń'),
        (CLIENT, 'Zwykły klient')]

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
        return reverse('user_detail', kwargs={'pk': self.pk})

    def get_details_list(self):
        fields = ['company_name', 'address', 'city', 'postcode', 'primary_phone', 'secondary_phone']
        data = []

        data.append(('klient', self.get_full_name()))

        for field in fields:
            value = getattr(self, field, None)
            if value:
                data.append((self._meta.get_field(field).verbose_name, value))
        return data

    @property
    def phone_numbers(self):
        if self.secondary_phone:
            return "%s, %s" % (self.primary_phone, self.secondary_phone)
        return self.primary_phone

