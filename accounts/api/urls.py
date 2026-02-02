# accounts/urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile
    path('profile/', ProfileDetailView.as_view(), name='user-profile'),

    # Addresses
    path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<int:id>/', AddressDetailView.as_view(), name='address-detail'),
    path('addresses/<int:id>/set-default/', SetDefaultAddressView.as_view(), name='set-default-address'),
]