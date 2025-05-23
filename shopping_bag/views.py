from .serializers import ShippingDetailSerializer, ShoppingBagSerializer, ShoppingBagDetailSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import ShoppingBagDetail, ShoppingBag, ShippingDetail
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from online_shop_api.pagination import CustomPaginationClass
from rest_framework.decorators import action
from rest_framework.response import Response


class ShoppingBagViewSet(ModelViewSet):
    queryset = ShoppingBag.objects.all()
    serializer_class = ShoppingBagSerializer
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ShoppingBag.objects.all()
        if self.request.user.is_authenticated:
            return ShoppingBag.objects.filter(user=self.request.user)
        return ShoppingBag.objects.none()

    def get_permissions(self):
        if self.request.user.is_superuser:
            return [IsAdminUser()]
        if self.request.user.is_authenticated:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(methods=['get'], permission_classes=[IsAuthenticated], detail=False)
    def current_shopping_bag(self, request):
        shopping_bag = ShoppingBag.objects.filter(user=request.user, is_active=True).first()
        if shopping_bag:
            return Response(ShoppingBagSerializer(shopping_bag).data, status=status.HTTP_200_OK)
        else:
            return Response({'message:': 'user does not have a shopping bag!'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShoppingBagDetailViewSet(ModelViewSet):
    queryset = ShoppingBagDetail.objects.all()
    serializer_class = ShoppingBagDetailSerializer
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ShoppingBagDetail.objects.all()
        if self.request.user.is_authenticated:
            return ShoppingBagDetail.objects.filter(
                shopping_bag=ShoppingBag.objects.filter(user=self.request.user, is_active=True))
        return ShoppingBagDetail.objects.none()

    def get_permissions(self):
        if self.request.user.is_superuser:
            return [IsAdminUser()]
        if self.request.user.is_authenticated:
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(shopping_bag=ShoppingBag.objects.filter(user=self.request.user, is_active=True).first())


class ShippingDetailViewSet(ModelViewSet):
    queryset = ShippingDetail.objects.all()
    serializer_class = ShippingDetailSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ShippingDetail.objects.all()
        if self.request.user.is_authenticated:
            self.request.user.shopping_bags.filter(is_active=True).first().shipping_detail.all()
        return ShippingDetail.objects.none()

    def get_permissions(self):
        if self.request.user.is_superuser:
            return [IsAdminUser()]
        if self.request.user.is_authenticated:
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(shopping_bag=self.request.user.shopping_bags.get(is_active=True))
