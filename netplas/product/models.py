from django.utils.translation import ugettext_lazy as _
from django.db import models
from stock.models import Stock


class Product(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    name = models.CharField(_('Ürün İsmi'), null=True, blank=True, max_length=150)
    created_at = models.DateTimeField('Kayıt Tarihi', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField('Güncellenme Tarihi', auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Ürün')
        verbose_name_plural = _('Ürünler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)
