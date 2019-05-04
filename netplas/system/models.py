from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from system.constant import *
from product.models import Product, Raw
from profile.models import UserProfile
from decimal import Decimal


class Client(models.Model):
    email = models.EmailField(_('E-posta'), unique=True, null=False, blank=False)
    name = models.CharField(_('İsim'), null=True, blank=True, max_length=150)
    surname = models.CharField(_('Soyisim'), null=True, blank=True, max_length=75)
    phone = models.CharField(_('Telefon'), null=True, blank=True, max_length=75)
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Müşteri')
        verbose_name_plural = _('Müşteriler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)


class Supplier(models.Model):
    email = models.EmailField(_('E-posta'), unique=True, null=False, blank=False)
    name = models.CharField(_('İsim'), null=True, blank=True, max_length=150)
    surname = models.CharField(_('Soyisim'), null=True, blank=True, max_length=75)
    phone = models.CharField(_('Telefon'), null=True, blank=True, max_length=75)
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Tedarikçi')
        verbose_name_plural = _('Tedarikçiler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)


class ProductOrder(models.Model):
    client = models.ForeignKey(Client, verbose_name=_('Müşteri'), null=False, blank=False,
                               on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_('Ürün'), null=False, blank=False,
                                on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name=_('Kullanıcı'), null=True, blank=True,
                             on_delete=models.CASCADE)
    name = models.CharField(_('Ürün İsmi'), null=True, blank=True, max_length=150)
    quantity = models.DecimalField(_('Siparişteki Ürün Sayısı'), null=True, blank=True, decimal_places=2,
                                   max_digits=10)
    total = models.DecimalField(_('Siparişin Toplam Fiyatı'), null=True, blank=True, decimal_places=2, max_digits=10)
    status = models.CharField(_('Ürün Siparişin Durumu'), choices=PRODUCT_ORDER_STATUS, default=WAITING, max_length=150)
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Ürün Siparişi')
        verbose_name_plural = _('Ürün Siparişleri')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)


class RawOrder(models.Model):
    supplier = models.ForeignKey(Supplier, verbose_name=_('Tedarikçi'), null=False, blank=False,
                                 on_delete=models.CASCADE)
    raw = models.ForeignKey(Raw, verbose_name=_('Ham madde'), null=False, blank=False,
                            on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name=_('Kullanıcı'), null=True, blank=True,
                             on_delete=models.CASCADE)
    name = models.CharField(_('Ham madde İsmi'), null=True, blank=True, max_length=150)
    quantity = models.DecimalField(_('Siparişteki Ham madde Sayısı'), null=True, blank=True, decimal_places=2,
                                   max_digits=10)
    total = models.DecimalField(_('Siparişin Toplam Maliyeti'), null=True, blank=True, decimal_places=2, max_digits=10)
    status = models.CharField(_('Ham madde Siparişin Durumu'), choices=RAW_ORDER_STATUS, default=WAITING,
                              max_length=150)
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Hammadde Siparişi')
        verbose_name_plural = _('Hammadde Siparişleri')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)


class Budget(models.Model):
    product_order = models.ForeignKey(ProductOrder, verbose_name=_('Ürün Siparişi'), null=True, blank=True,
                                      on_delete=models.CASCADE)
    raw_order = models.ForeignKey(RawOrder, verbose_name=_('Hammadde Siparişi'), null=True, blank=True,
                                  on_delete=models.CASCADE)
    total_income = models.DecimalField(_('Toplam Gelir'), null=True, blank=True, decimal_places=2, max_digits=10)
    total_outcome = models.DecimalField(_('Toplam Gider'), null=True, blank=True, decimal_places=2, max_digits=10)
    total = models.DecimalField(_('Genel Toplam'), null=True, blank=True, decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(_('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Gelir/Gider')
        verbose_name_plural = _('Gelirler/Giderler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.total)


@receiver(pre_save, sender=ProductOrder)
def set_product_order_total(sender, instance, **kwargs):
    instance.total = instance.product.unit_price * instance.quantity


@receiver(pre_save, sender=RawOrder)
def set_raw_order_total(sender, instance, **kwargs):
    instance.total = instance.raw.unit_price * instance.quantity


@receiver(post_save, sender=ProductOrder)
def set_product_order_budget(sender, instance, **kwargs):
    print(instance)
    budget_instance = Budget(product_order=instance)
    budget_instance.save()


@receiver(post_save, sender=RawOrder)
def set_raw_order_budget(sender, instance, **kwargs):
    budget_instance = Budget(raw_order=instance)
    budget_instance.save()


@receiver(pre_save, sender=Budget)
def set_income_total(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.id is None:
        total_income = Budget.objects.all().exclude(product_order__isnull=True).first()

        if total_income is not None:
            if instance.product_order:
                instance.total_income = Decimal(total_income.total_income + instance.product_order.product.unit_price *
                                                instance.product_order.quantity)
        else:
            if instance.product_order:
                instance.total_income = Decimal(instance.product_order.product.unit_price *
                                                instance.product_order.quantity)


@receiver(pre_save, sender=Budget)
def set_outcome_total(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.id is None:
        total_outcome = Budget.objects.all().exclude(raw_order__isnull=True).first()

        if total_outcome is not None:
            if instance.raw_order:
                instance.total_outcome = Decimal(total_outcome.total_outcome - instance.raw_order.raw.unit_price
                                                 * instance.raw_order.quantity)
        else:
            if instance.raw_order:
                instance.total_outcome = Decimal(0 - instance.raw_order.raw.unit_price
                                                 * instance.raw_order.quantity)


@receiver(pre_save, sender=Budget)
def set_budget_total(sender, instance, **kwargs):
    total_outcome = Budget.objects.all().exclude(raw_order__isnull=True).first()
    total_income = Budget.objects.all().exclude(product_order__isnull=True).first()
    instance.total = total_income.total_income + total_outcome.total_outcome
