from django.urls import path
from .views import CustomLogoutView, LogoutView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
]
