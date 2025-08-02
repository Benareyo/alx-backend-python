from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # Routes to your chats app
    path('api-auth/', include('rest_framework.urls')),  # For browsable API login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]
