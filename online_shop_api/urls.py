from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(

    openapi.Info(
        title='Online Shop API',
        default_version='v1',
        description='API for Online Shop',
        contact=openapi.Contact(email='reza@reza.com'),
        license=openapi.License(name='MIT License'),
    )
    ,
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # apps
    path('', include('core.urls')),
    path('', include('users.urls')),
    path('', include('products.urls')),
    path('', include('categories.urls')),
    path('', include('reviews.urls')),
    path('', include('shopping_bag.urls')),
    # api Documentation
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    # Token Urls
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
