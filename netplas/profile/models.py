from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from profile.managers import AmbarUserManager
from profile.constant import *
from decimal import Decimal


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('E-posta'), unique=True, null=False, blank=False)
    name = models.CharField(_('İsim'), null=True, blank=True, max_length=75)
    surname = models.CharField(_('Soyisim'), null=True, blank=True, max_length=75)
    tckn = models.CharField(_('TC Kimlik Numarası'), max_length=11, null=True, blank=True)
    phone = models.CharField(_('Telefon Numarası'), null=True, blank=True, max_length=15)
    type = models.CharField(_('Yetki Seviyesi'), choices=PERSONEL_TYPE, default=WORKER,  max_length=150)
    salary = models.DecimalField(_('Personel Maaşı'), null=True, blank=True, decimal_places=2, max_digits=10,
                                 default=Decimal(0))
    is_staff = models.BooleanField(_('Staff Status'), default=False)
    is_manager = models.BooleanField(_('Manager'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    USERNAME_FIELD = 'email'
    objects = AmbarUserManager()

    class Meta:
        verbose_name = _('Firma Personeli')
        verbose_name_plural = _('Firma Personelleri')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.email)

    @property
    def full_name(self):
        return '{}'.format(self.email)
