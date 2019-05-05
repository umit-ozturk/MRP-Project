from django.utils.translation import ugettext_lazy as _
from django.db import models
from stock.models import ProductStock, RawStock


class Raw(models.Model):
    stock = models.ForeignKey(RawStock, on_delete=models.CASCADE, verbose_name=_('Ham madde Deposu'))
    name = models.CharField(_('Hammadde İsmi'), null=True, blank=True, max_length=150)
    unit_price = models.DecimalField(_('Hammaddenin Birim Fiyatı'), null=True, blank=True, decimal_places=2,
                                     max_digits=10)
    amount = models.DecimalField(_('Ambalajtaki Ham madde Sayısı'), null=True, blank=True, decimal_places=2,
                                 max_digits=10)
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Ham madde')
        verbose_name_plural = _('Ham maddeler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)


class RawForProduction(models.Model):
    raw = models.ManyToManyField(Raw, verbose_name=_('Ham madde Deposu'))
    quantity_for_prod = models.IntegerField(_('Üretim için Gereken Ham maddenin Miktari'))
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Üretim için Ham Madde Miktarı')
        verbose_name_plural = _('Üretim için Ham Madde Miktarları')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.raw.name)


class Product(models.Model):
    raw_for_prod = models.ForeignKey(RawForProduction, on_delete=models.CASCADE,
                                     verbose_name=_('Ürünün Üretilmesi için Gerekli Ham Maddeler'))
    stock = models.ForeignKey(ProductStock, on_delete=models.CASCADE, verbose_name=_('Ürün Deposu'))
    name = models.CharField(_('Ürün İsmi'), null=True, blank=True, max_length=150)
    unit_price = models.DecimalField(_('Ürünün Birim Fiyati'), null=True, blank=True, decimal_places=2, max_digits=10)
    amount = models.DecimalField(_('Ambalajdaki Ürün Sayısı'), null=True, blank=True, decimal_places=2,
                                 max_digits=10)
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Ürün')
        verbose_name_plural = _('Ürünler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)


class DamagedRaw(models.Model):
    raw = models.ForeignKey(Raw, on_delete=models.CASCADE, verbose_name=_('Ham madde'))
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Hasarlı Ham madde')
        verbose_name_plural = _('Hasarlı Ham maddeler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.raw.name)


class DamagedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Ürün'))
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Hasarlı Ürün')
        verbose_name_plural = _('Hasarlı Ürünler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.product.name)
