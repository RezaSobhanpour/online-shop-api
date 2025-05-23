from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import ShoppingBagViewSet, ShippingDetailViewSet, ShoppingBagDetailViewSet

router = DefaultRouter()
router.register(r'shopping-bag', ShoppingBagViewSet, basename='shopping-bag')
router.register(r'shopping-bag-detail', ShoppingBagDetailViewSet, basename='shopping-bag-detail')
router.register(r'shipping-detail', ShippingDetailViewSet, basename='shipping-detail')

urlpatterns = [
    path('', include(router.urls)),
]
