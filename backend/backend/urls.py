from django.contrib import admin
from django.urls import path, include
from accounts.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/', include('students.urls')),
    path('/', include('accounts.urls')),
    path('api/logout/', LogoutView.as_view(), name='logout')
]
