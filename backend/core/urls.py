from django.urls import path
from . import views

# No app_name — these are pure API endpoints, no Django URL reversing needed.
urlpatterns = [
    # Health
    path('api/health/',   views.health_check,   name='health'),

    # Auth
    path('api/signup/',   views.signup,          name='signup'),
    path('api/login/',    views.login_view,       name='login'),
    path('api/logout/',   views.logout_view,      name='logout'),
    path('api/me/',       views.me,               name='me'),

    # Data
    path('api/symbols/',  views.symbols,          name='symbols'),
    path('api/calendar/', views.calendar_events,  name='calendar'),
]
