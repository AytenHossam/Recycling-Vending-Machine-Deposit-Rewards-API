from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterView, UserLoginView, AdminRegisterView, AdminLoginView,
    DepositView, SummaryView, DepositInfoView, MachineViewSet, AdminDepositListView
)

router = DefaultRouter()
router.register(r'machines', MachineViewSet, basename='machine')

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('summary/', SummaryView.as_view(), name='summary'),
    path('deposit-info/', DepositInfoView.as_view(), name='deposit-info'),
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/deposits/', AdminDepositListView.as_view(), name='admin-deposits'),
    path('', include(router.urls)),
] 