from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from online_shop_api.pagination import CustomPaginationClass


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPaginationClass
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['name', 'price', 'created_at']
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Product.objects.filter(is_active=True)

    def get_object(self):
        try:
            obj = super().get_object()
            return obj
        except Http404:
            raise
