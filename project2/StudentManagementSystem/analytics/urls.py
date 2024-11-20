from django.urls import path
from .views import ActiveUsersView

urlpatterns = [
    path('active-users/', ActiveUsersView.as_view(), name='active-users'),
]