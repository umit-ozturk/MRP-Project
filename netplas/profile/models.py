from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from profile.managers import AmbarUserManager
from profile.constant import *


class FirmPersonel(models.Model):
    tckn = models.CharField('TKCN', max_length=11, null=True, blank=True)
    phone = models.CharField('Telefon Numarası', null=True, blank=True, max_length=15)
    type = models.CharField('Yetki Seviyesi', choices=PERSONEL_TYPE, default=WORKER,  max_length=150)
    created_at = models.DateTimeField('Kayıt Tarihi', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Firma Personeli'
        verbose_name_plural = 'Firma Personelleri'
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.type)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    firm_personel = models.ForeignKey(FirmPersonel, verbose_name='Firma Yetkilisi', null=True, blank=True,
                                      related_name='users', on_delete=models.CASCADE)
    email = models.EmailField('E-posta', unique=True, null=False, blank=False)
    name = models.CharField('İsim', null=True, blank=True, max_length=75)
    surname = models.CharField('Soyisim', null=True, blank=True, max_length=75)
    is_staff = models.BooleanField('Staff Status', default=False)
    is_manager = models.BooleanField('Manager', default=False)
    is_active = models.BooleanField('Active', default=True)
    created_at = models.DateTimeField('Oluşturulma Tarihi', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True, editable=False)

    USERNAME_FIELD = 'email'
    objects = AmbarUserManager()

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.email)

    @property
    def full_name(self):
        return '{} {}'.format(self.name, self.surname)
