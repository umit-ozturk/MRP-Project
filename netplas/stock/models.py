from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import pre_save


class ProductStock(models.Model):
    name = models.CharField(_('Depo İsmi'), null=True,
                            blank=True, max_length=150)
    count = models.PositiveIntegerField(default=0)
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
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(
        _('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Ham madde Deposu')
        verbose_name_plural = _('Ham madde Depoları')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)


@receiver(pre_save, sender=ProductStock)
def set_product_stock_total(sender, instance, **kwargs):
    try:
        instance.count = instance.count + ProductStock.objects.filter(name=instance.name
                                                                      ).aggregate(Sum('count'))['count__sum']
    except:
        instance.count = 0


@receiver(pre_save, sender=RawStock)
def set_raw_stock_total(sender, instance, **kwargs):
    try:
        instance.count = instance.count + RawStock.objects.filter(name=instance.name
                                                                  ).aggregate(Sum('count'))['count__sum']
    except:
        instance.count = 0
