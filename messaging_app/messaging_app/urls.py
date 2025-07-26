from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
=======
    path('chats/', include('chats.urls')),
>>>>>>> 304ced478da411f5219fe2b9bd843517e7e0dce4
    path('api/', include('chats.urls')),  # Routes to your chats app
    path('api-auth/', include('rest_framework.urls')),  # For browsable API login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]
