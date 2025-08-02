from django.urls import path
from .views import delete_user

urlpatterns = [
    # ... other url patterns
    path('delete-account/', delete_user, name='delete_user'),
]
