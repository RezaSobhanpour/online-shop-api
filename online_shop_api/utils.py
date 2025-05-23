import uuid
from django.utils.text import slugify


def unique_slug(instance, title_field, slug_field='slug'):
    title = getattr(instance, title_field)
    slug = slugify(title)
    unique_slug = slug
    counter = 1

    instance_class = instance.__class__

    while instance_class.objects.filter(**{slug_field: unique_slug}).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug


def upload_to_product(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return f'product/{instance.product.id}/{filename}'
