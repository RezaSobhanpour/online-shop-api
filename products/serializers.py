from rest_framework import serializers
from .models import Product, ProductImage
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'primary', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)


class ProductSerializer(serializers.ModelSerializer):
    all_rating = ReviewSerializer(source='reviews', many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    images = ImageSerializer(many=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['title', 'slug', 'price', 'discount_price', 'description', 'categories', 'uuid', 'stock',
                  'created_at',
                  'updated_at', 'is_active', 'avg_rating', 'all_rating', 'in_stock', 'images']
        extra_kwargs = {
            'uuid': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def get_avg_rating(self, obj):
        return obj.rating

    def get_in_stock(self, obj):
        return obj.in_stock()

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        return product
