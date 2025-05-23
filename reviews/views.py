from .permissions import IsOwnerOrAdmin
from .serializers import ReviewSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Review
from online_shop_api.pagination import CustomPaginationClass


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['product__title', 'user__username', 'body']
    ordering_fields = ['created_at', 'rating']
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        queryset = Review.objects.select_related('user', 'product')

        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset.filter(product__id=product_id)

        if self.request.query_params.get('mine') and self.request.user.is_authenticated:
            queryset.filter(user=self.request.user)

        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
