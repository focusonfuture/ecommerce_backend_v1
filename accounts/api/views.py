# accounts/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import CustomUser, Address
from .serializers import (
    UserProfileSerializer,
    AddressSerializer,
    AddressCreateUpdateSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.api.serializers import CustomTokenObtainPairSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
            },
            "message": "User created successfully",
        }, status=status.HTTP_201_CREATED)
    

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    GET     → Get current user profile
    PATCH   → Update profile (first_name, last_name, gender, phone)
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # PATCH support
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AddressListCreateView(generics.ListCreateAPIView):
    """
    GET     → List all addresses of logged-in user
    POST    → Create new address
    """
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddressCreateUpdateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET     → Retrieve single address
    PATCH   → Update address
    DELETE  → Delete address
    """
    serializer_class = AddressCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Address deleted successfully"},
            status=status.HTTP_200_OK
        )


class SetDefaultAddressView(APIView):
    """
    POST /addresses/<id>/set-default/
    Sets the given address as default (and removes default from others)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            address = Address.objects.get(id=id, user=request.user)
        except Address.DoesNotExist:
            return Response(
                {"error": "Address not found or not owned by you"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Remove default from all other addresses
        Address.objects.filter(user=request.user, is_default=True).exclude(id=address.id).update(is_default=False)

        address.is_default = True
        address.save()

        return Response(
            {"message": "Default address updated successfully"},
            status=status.HTTP_200_OK
        )