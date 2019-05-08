from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from system.constant import *
from product.models import Product, Raw, RawForProduction
from profile.models import UserProfile
from decimal import Decimal
from django.contrib.postgres.fields import JSONField


class Client(models.Model):
    email = models.EmailField(
        _('E-posta'), unique=True, null=False, blank=False)
    name = models.CharField(_('İsim'), null=True, blank=True, max_length=150)
    surname = models.CharField('Soyisim', null=True, blank=True, max_length=75)
    phone = models.CharField('Telefon', null=True, blank=True, max_length=75)
    created_at = models.DateTimeField(
        _('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Müşteri')
        verbose_name_plural = _('Müşteriler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.name)


class Supplier(models.Model):
    email = models.EmailField(
        _('E-posta'), unique=True, null=False, blank=False)
    name = models.CharField(_('İsim'), null=True, blank=True, max_length=150)
    surname = models.CharField('Soyisim', null=True, blank=True, max_length=75)
    phone = models.CharField('Telefon', null=True, blank=True, max_length=75)
    created_at = models.DateTimeField(
        _('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'), auto_now=True, editable=False)

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
    personal = models.ForeignKey(UserProfile, verbose_name=_('Kullanıcı'), null=True, blank=True,
                                 on_delete=models.CASCADE)
    order_title = models.CharField(
        _('Sipariş Başlığı'), null=True, blank=True, max_length=150)
    quantity = models.DecimalField(
        _('Siparişteki Ürün Sayısı'), null=True, blank=True, decimal_places=2, max_digits=10, default=Decimal(1))
    actual_quantity = models.DecimalField(_('Gerçekleştirilen Siparişteki Ürün Sayısı'), null=True, blank=True,
                                          decimal_places=2, max_digits=10, default=Decimal(0))
    status = models.CharField(_('Ürün Siparişin Durumu'),
                              choices=PRODUCT_ORDER_STATUS, default=WAITING, max_length=150)
    created_at = models.DateTimeField(
        _('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'), auto_now=True, editable=False)
    data = JSONField(blank=True, null=True)
    total = models.DecimalField(
        _('Siparişin Toplam Fiyatı'), null=True, blank=True, decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = _('Ürün Siparişi')
        verbose_name_plural = _('Ürün Siparişleri')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.product.name)


class RawOrder(models.Model):
    supplier = models.ForeignKey(Supplier, verbose_name=_('Tedarikçi'), null=False, blank=False,
                                 on_delete=models.CASCADE)
    raw = models.ForeignKey(Raw, verbose_name=_('Ham madde'), null=False, blank=False,
                            on_delete=models.CASCADE)
    personal = models.ForeignKey(UserProfile, verbose_name=_('Kullanıcı'), null=True, blank=True,
                                 on_delete=models.CASCADE)
    order_title = models.CharField(
        _('Sipariş Başlığı'), null=True, blank=True, max_length=150)
    quantity = models.DecimalField(_('Siparişteki Ham madde Sayısı'), null=True, blank=True, decimal_places=2,
                                   max_digits=10, default=Decimal(1))
    actual_quantity = models.DecimalField(_('Gerçekleştirilen Siparişteki Ham Madde Sayısı'), null=True, blank=True,
                                          decimal_places=2, max_digits=10, default=Decimal(0))
    status = models.CharField(_('Hammadde Siparişin Durumu'),
                              choices=RAW_ORDER_STATUS, default=WAITING, max_length=150)
    created_at = models.DateTimeField(
        _('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'), auto_now=True, editable=False)
    data = JSONField(blank=True, null=True)
    total = models.DecimalField(_('Siparişin Toplam Maliyeti'),
                                null=True, blank=True, decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = _('Hammadde Siparişi')
        verbose_name_plural = _('Hammadde Siparişleri')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.raw.name)


class Budget(models.Model):
    product_order = models.ForeignKey(ProductOrder, verbose_name=_('Ürün Siparişi'), null=True, blank=True,
                                      on_delete=models.CASCADE)
    raw_order = models.ForeignKey(RawOrder, verbose_name=_('Hammadde Siparişi'), null=True, blank=True,
                                  on_delete=models.CASCADE)
    total_income = models.DecimalField(
        _('Toplam Gelir'), null=True, blank=True, decimal_places=2, max_digits=10, default=Decimal(0))
    total_outcome = models.DecimalField(
        _('Toplam Gider'), null=True, blank=True, decimal_places=2, max_digits=10, default=Decimal(0))
    salaries = models.DecimalField(
        _('Maaşlar'), null=True, blank=True, decimal_places=2, max_digits=10, default=Decimal(0))
    total = models.DecimalField(
        _('Genel Toplam'), null=True, blank=True, decimal_places=2, max_digits=10, default=Decimal(0))
    created_at = models.DateTimeField(
        _('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Gelir/Gider')
        verbose_name_plural = _('Gelirler/Giderler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.total)


class DamagedRaw(models.Model):
    raw_order = models.ForeignKey(RawOrder, on_delete=models.CASCADE, verbose_name=_('Ham madde Siparişi'))
    raw = models.ForeignKey(Raw, on_delete=models.CASCADE,
                            verbose_name=_('Ham madde'))
    created_at = models.DateTimeField(
        _('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Hasarlı Ham madde')
        verbose_name_plural = _('Hasarlı Ham maddeler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.raw.name)


class DamagedProduct(models.Model):
    product_order = models.ForeignKey(ProductOrder, on_delete=models.CASCADE, verbose_name=_('Ham madde Siparişi'))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_('Ürün'))
    created_at = models.DateTimeField(
        _('Kayıt Tarihi'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Hasarlı Ürün')
        verbose_name_plural = _('Hasarlı Ürünler')
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.product.name)


"""

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
"""


@receiver(pre_save, sender=ProductOrder)
def set_product_order_total(sender, instance, **kwargs):
    instance.total = instance.product.unit_price * instance.quantity


@receiver(pre_save, sender=RawOrder)
def set_raw_order_total(sender, instance, **kwargs):
    instance.total = instance.raw.unit_price * instance.quantity


@receiver(post_save, sender=RawOrder)
def set_budget_raw(sender, instance, **kwargs):
    if instance.status == SUCCESS:
        budget = Budget.objects.filter()
        if budget.exists():
            total = budget.first().total
        else:
            total = 0
        Budget.objects.create(
            raw_order=instance,
            total_outcome=instance.total,
            total=total - instance.total
        )


@receiver(post_save, sender=ProductOrder)
def set_budget(sender, instance, **kwargs):
    if instance.status == SUCCESS:
        budget = Budget.objects.filter()
        if budget.exists():
            total = budget.first().total
        else:
            total = 0
        Budget.objects.create(
            product_order=instance,
            total_income=instance.total,
            total=total + instance.total
        )


@receiver(post_save, sender=ProductOrder)
def add_product_stock(sender, instance, **kwargs):
    if instance.status == SUCCESS:
        instance.product.stock.count += instance.quantity
        instance.product.stock.save()


@receiver(post_save, sender=ProductOrder)
def remove_raw_stock(sender, instance, **kwargs):
    if instance.status == WAITING and kwargs['created']:
        raws = instance.product.raws.all()
        for raw in raws:
            total = instance.quantity * Decimal(raw.quantity_for_prod)
            raw.raw.stock.count -= total
            raw.raw.stock.save()


@receiver(post_save, sender=RawOrder)
def add_raw_stock(sender, instance, **kwargs):
    if instance.status == SUCCESS:
        instance.raw.stock.count += instance.quantity
        instance.raw.stock.save()


@receiver(pre_save, sender=Budget)
def set_budget_for_salaries(sender, instance, **kwargs):
    if instance.salaries:
        instance.total -= instance.salaries
