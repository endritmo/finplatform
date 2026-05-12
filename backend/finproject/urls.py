from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Django admin (still useful for managing data)
    path('admin/', admin.site.urls),

    # JWT token refresh endpoint
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App API routes
    path('', include('core.urls')),
    path('ai/', include('ai_assistant.urls')),
    path('api/forum/', include('forum.urls')),
]
