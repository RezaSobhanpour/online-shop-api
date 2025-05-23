from django.db import models
from django.utils.text import gettext_lazy as _
from users.models import User


class Review(models.Model):
    RATING_CHOICES = (
        (0, 'not rated'),
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'), related_name='reviews')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name=_('Product'),
                                related_name='reviews', db_index=True)
    body = models.TextField(verbose_name=_('Body'), null=True, blank=True)
    rating = models.SmallIntegerField(choices=RATING_CHOICES, default=0, verbose_name=_('Rating'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'), db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.rating}'

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at']
        unique_together = ['product', 'user']
