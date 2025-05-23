import uuid
from django.db import models
from django.utils.text import gettext_lazy as _
from categories.models import Category
from online_shop_api.utils import upload_to_product, unique_slug
from reviews.models import Review


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), blank=True, null=True, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Price'), default=0)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Discount Price'), default=0)
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    categories = models.ManyToManyField(Category, verbose_name=_('Categories'),
                                        related_name='products')
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False, verbose_name=_('UUID'))
    stock = models.PositiveIntegerField(default=0, verbose_name=_('Stock'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs, ):
        if not self.slug:
            self.slug = unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    @property
    def rating(self):
        product_reviews = Review.objects.filter(product=self)
        if not product_reviews.exists():
            return 0
        return sum(review.rating for review in product_reviews) / product_reviews.count()

    def in_stock(self):
        return self.stock > 0


class ProductImage(models.Model):
    image = models.ImageField(upload_to=upload_to_product, verbose_name=_('Image'))
    primary = models.BooleanField(default=False, verbose_name=_('Primary'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'), related_name='images')

    def __str__(self):
        return f'{self.pk}-{self.product.title}'

    def save(self, *args, **kwargs):
        if self.primary:
            ProductImage.objects.filter(product=self.product).exclude(pk=self.pk).update(primary=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['product']
