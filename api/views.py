from rest_framework import generics, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Machine, Deposit, AdminProfile
from .serializers import (
    UserRegisterSerializer, AdminRegisterSerializer, MachineSerializer,
    DepositSerializer, DepositInfoSerializer, SummarySerializer
)
from .permissions import IsAdminUser, IsNormalUser
from .utils import calculate_points
from django.shortcuts import get_object_or_404

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class AdminRegisterView(generics.CreateAPIView):
    serializer_class = AdminRegisterSerializer
    permission_classes = [permissions.AllowAny]

class AdminLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_staff:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'detail': 'Invalid admin credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class DepositView(generics.CreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = [IsNormalUser]
    def perform_create(self, serializer):
        material_type = self.request.data.get('material_type')
        weight = float(self.request.data.get('weight', 0))
        points = calculate_points(material_type, weight)
        serializer.save(user=self.request.user, points=points)

class SummaryView(APIView):
    permission_classes = [IsNormalUser]
    def get(self, request):
        deposits = Deposit.objects.filter(user=request.user)
        plastic_weight = sum(d.weight for d in deposits if d.material_type == 'plastic')
        metal_weight = sum(d.weight for d in deposits if d.material_type == 'metal')
        glass_weight = sum(d.weight for d in deposits if d.material_type == 'glass')
        total_points = round(sum(d.points for d in deposits), 1)
        serializer = SummarySerializer({
            'plastic_weight': plastic_weight,
            'metal_weight': metal_weight,
            'glass_weight': glass_weight,
            'total_points': total_points
        })
        return Response(serializer.data)

class DepositInfoView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        machines = Machine.objects.all()
        machine_serializer = DepositInfoSerializer(machines, many=True)
        reward_rates = {'plastic': 1, 'metal': 3, 'glass': 2}
        return Response({
            'machines': machine_serializer.data,
            'reward_rates': reward_rates
        })

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [IsAdminUser]

class AdminDepositListView(generics.ListAPIView):
    serializer_class = DepositSerializer
    permission_classes = [IsAdminUser]
    queryset = Deposit.objects.all()
