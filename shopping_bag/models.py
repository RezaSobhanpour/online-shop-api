from django.db import models
from products.models import Product
from django.utils.text import gettext_lazy as _
from users.models import User


class ShoppingBag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_bags', verbose_name=_('User'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    @property
    def total_price(self):
        shopping_bag_details = self.shopping_bag_details.all()
        total_price = 0

        for shopping_bag_detail in shopping_bag_details:
            total_price += shopping_bag_detail.total_price
        return total_price

    def __str__(self):
        return f'{self.user.get_full_name()} Shopping Bag'

    def save(self, *args, **kwargs):
        if not self.pk and ShoppingBag.objects.filter(user=self.user, is_active=True).exists():
            raise ValueError(_('User already has an active shopping bag'))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Shopping Bag')
        verbose_name_plural = _('Shopping Bags')
        indexes = [models.Index(fields=['user', 'is_active'])]
        ordering = ['-created_at']


class ShoppingBagDetail(models.Model):
    shopping_bag = models.ForeignKey(ShoppingBag, on_delete=models.CASCADE, verbose_name=_('Shopping Bag'),
                                     related_name='shopping_bag_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'),
                                related_name='shopping_bags')
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.shopping_bag.user.get_full_name()}-{self.product.title}'

    class Meta:
        verbose_name = _('Shopping Bag Detail')
        verbose_name_plural = _('Shopping Bag Details')
        unique_together = ['shopping_bag', 'product']
        ordering = ['-created_at']


SHIPPING_METHOD = (
    ('standard', _('Standard Shipping (3-5 days)')),
    ('pishtaz', _('Express Shipping (1-2 days)')),
    ('in_city', _('Same-day Delivery (in city)')),
)


class ShippingDetail(models.Model):
    shopping_bag = models.OneToOneField(ShoppingBag, on_delete=models.CASCADE, related_name='shipping_detail',
                                        verbose_name=_('Shopping Bag'))
    recipient_name = models.CharField(max_length=255, verbose_name=_('Recipient Name'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone Number'))
    address = models.CharField(max_length=400, verbose_name=_('Address'), )
    city = models.CharField(max_length=255, verbose_name=_('City'))
    province = models.CharField(max_length=255, verbose_name=_('Province'))
    postal_code = models.CharField(max_length=20, verbose_name=_('Postal Code'))
    country = models.CharField(max_length=255, verbose_name=_('Country'))

    shipping_method = models.CharField(max_length=255, verbose_name=_('Shipping Method'), choices=SHIPPING_METHOD)

    def __str__(self):
        return f'{self.shopping_bag.user.get_full_name()}-Shipping Address'

    class Meta:
        verbose_name = _('Shipping Detail')
        verbose_name_plural = _('Shipping Details')
        ordering = ['-shopping_bag__created_at']
