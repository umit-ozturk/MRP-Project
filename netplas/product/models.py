from django.utils.translation import ugettext_lazy as _
from django.db import models
from stock.models import ProductStock, RawStock


class Product(models.Model):
    stock = models.ForeignKey(ProductStock, on_delete=models.CASCADE, verbose_name=_('Ürün Deposu'))
    name = models.CharField(_('Ürün İsmi'), null=True, blank=True, max_length=150)
    quantity = models.PositiveIntegerField(_('Ürün Adeti'), null=True, blank=True)
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Ürün')
        verbose_name_plural = _('Ürünler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)


class Raw(models.Model):
    stock = models.ForeignKey(RawStock, on_delete=models.CASCADE, verbose_name=_('Hammadde Deposu'))
    name = models.CharField(_('Hammadde İsmi'), null=True, blank=True, max_length=150)
    quantity = models.PositiveIntegerField(_('Hammadde Adeti'), null=True, blank=True)
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Hammadde')
        verbose_name_plural = _('Hammaddeler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)