from django.contrib import admin   
from django.urls import path, include
from .views import login_page, register_page, dashboard_page

urlpatterns = [
    path('admin/', admin.site.urls),   

    path('', login_page),
    path('register/', register_page),
    path('dashboard/', dashboard_page),

    # API routes
    path('api/auth/', include('users.urls')),
    path('api/records/', include('records.urls')),
    path('api/dashboard/', include('dashboard.urls')),
]