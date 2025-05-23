from django.db import models
from django.utils.text import gettext_lazy as _
from online_shop_api.utils import unique_slug


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, verbose_name=_('Parent'),
                               related_name='child_categories', null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'), db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['created_at']
