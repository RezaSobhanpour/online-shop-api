from django.contrib import admin
from .models import ShoppingBag, ShoppingBagDetail, ShippingDetail
from users.models import User


class ShoppingBagAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'is_active')

    def has_add_permission(self, request):
        if request.user.shopping_bags.filter(is_active=True).exists():
            return False
        return True


class ShoppingBagDetailAdmin(admin.ModelAdmin):
    list_display = ('shopping_bag', 'product', 'quantity', 'total_price')


class ShippingDetailAdmin(admin.ModelAdmin):
    list_display = (
        'shopping_bag', 'recipient_name', 'phone_number',
        'city', 'province', 'postal_code', 'country', 'shipping_method'
    )


admin.site.register(ShoppingBag, ShoppingBagAdmin)
admin.site.register(ShoppingBagDetail, ShoppingBagDetailAdmin)
admin.site.register(ShippingDetail, ShippingDetailAdmin)
