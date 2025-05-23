from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import ShoppingBag, ShoppingBagDetail, ShippingDetail, SHIPPING_METHOD
from users.models import User
from products.models import Product
from products.serializers import ProductSerializer


class ShoppingBagSerializer(ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(write_only=True, default=serializers.CurrentUserDefault(),
                                              queryset=User.objects.all())
    user_name = serializers.SerializerMethodField()
    details_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ShoppingBag
        fields = [
            'id',
            'user',
            'user_name',
            'created_at',
            'updated_at',
            'is_active',
            'total_price',
            'details_count'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'total_price',
            'user_name',
            'details_count'
        ]

    def get_total_price(self, obj):
        return obj.total_price

    def get_user_name(self, obj):
        return obj.user.get_full_name()

    def get_details_count(self, obj):
        return obj.shopping_bag_details.count()


class ShoppingBagDetailSerializer(ModelSerializer):
    shopping_bag = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ShoppingBag.objects.all())

    product = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all())
    product_detail = ProductSerializer(read_only=True)

    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ShoppingBagDetail
        fields = [
            'id',
            'shopping_bag',
            'product',
            'product_detail',
            'quantity',
            'created_at',
            'updated_at',
            'total_price'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'total_price',
            'product_detail'
        ]

    def get_total_price(self, obj):
        return obj.total_price

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('quantity must be greater than 0')
        return value

    def validate(self, attrs):
        if not self.instance and ShoppingBagDetail.objects.filter(
                shopping_bag=attrs['shopping_bag'],
                product=attrs['product']
        ).exists():
            raise serializers.ValidationError('product already exists in shopping bag')
        return attrs


class ShippingDetailSerializer(ModelSerializer):
    shopping_bag = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ShoppingBag.objects.all())

    class Meta:
        model = ShippingDetail
        fields = [
            'id',
            'shopping_bag',
            'recipient_name',
            'phone_number',
            'address',
            'city',
            'province',
            'postal_code',
            'country',
            'shipping_method'
        ]
        read_only_fields = [
            'id'
        ]

    def validate_shipping_method(self, value):
        shipping_method = [method[0] for method in SHIPPING_METHOD]
        if value not in shipping_method:
            raise serializers.ValidationError('shipping method does not exists!!')
        return value

    def validate_phone_number(self, value):
        if not len(value) > 10:
            raise serializers.ValidationError('phone number must be greater than 10')
        return value

    def validate_shopping_bag(self, value):
        if ShippingDetail.objects.filter(shopping_bag=value).exists():
            raise serializers.ValidationError('shipping detail already exists for this shopping bag')
        return value
