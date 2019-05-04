from django.utils.translation import ugettext_lazy as _
from django.db import models


class ProductStock(models.Model):
    name = models.CharField(_('Depo İsmi'), null=True,
                            blank=True, max_length=150)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(
        _('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Ürün Deposu')
        verbose_name_plural = _('Ürün Depoları')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)


class RawStock(models.Model):
    name = models.CharField(_('Depo İsmi'), null=True,
                            blank=True, max_length=150)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(
        _('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Hammadde Deposu')
        verbose_name_plural = _('Hammadde Depoları')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)
