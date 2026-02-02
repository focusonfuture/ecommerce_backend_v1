from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name', 'phone')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            username=validated_data.get('username', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'gender',
            'phone',
        ]
        read_only_fields = ['id', 'email']  # usually don't let user change email easily

    def validate_phone(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'address_type',
            'full_name',
            'phone',
            'alternate_phone',
            'pincode',
            'locality',
            'city',
            'state',
            'landmark',
            'is_default',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Optional: enforce at least one default address logic here if needed
        return data


class AddressCreateUpdateSerializer(AddressSerializer):
    """Used for create/update — can be more strict or relaxed"""
    pass