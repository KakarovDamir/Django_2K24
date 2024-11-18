from django.urls import path
from .views import AssignRoleView

urlpatterns = [
    path('assign-role/<int:pk>/', AssignRoleView.as_view(), name='assign-role'),
]

