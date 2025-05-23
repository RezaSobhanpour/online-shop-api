from rest_framework import serializers
from .models import Review
from rest_framework.validators import UniqueTogetherValidator
from users.models import User
from products.models import Product


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    product_title = serializers.SerializerMethodField(read_only=True)

    user = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(),
                                              default=serializers.CurrentUserDefault())
    product = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'product', 'product_title', 'body', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['product', 'user'],
                message="You have already reviewed this product."
            )
        ]

    def get_user_name(self, obj):
        if not obj.user:
            return 'Unknown user'
        return obj.user.get_full_name() or obj.username

    def get_product_title(self, obj):
        return obj.product.title if obj.product else 'Unknown product'

    def validate_rating(self, value):
        valid_rating = [choice[0] for choice in Review.RATING_CHOICES]
        if value not in valid_rating:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value
