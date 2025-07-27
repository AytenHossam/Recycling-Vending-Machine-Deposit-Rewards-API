from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Machine, Deposit, AdminProfile
from django.contrib.auth.password_validation import validate_password

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_staff=False
        )
        return user

class AdminRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    company_id = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'company_id')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        company_id = validated_data.pop('company_id')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_staff=True
        )
        AdminProfile.objects.create(user=user, company_id=company_id)
        return user

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'location', 'status']

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'user', 'machine', 'material_type', 'weight', 'points', 'timestamp']
        read_only_fields = ['user', 'points', 'timestamp']

    def validate_material_type(self, value):
        valid_types = dict(Deposit.MATERIAL_CHOICES).keys()
        if value not in valid_types:
            raise serializers.ValidationError("Invalid material type.")
        return value

class DepositInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'location', 'status']

class SummarySerializer(serializers.Serializer):
    plastic_weight = serializers.FloatField()
    metal_weight = serializers.FloatField()
    glass_weight = serializers.FloatField()
    total_points = serializers.FloatField() 