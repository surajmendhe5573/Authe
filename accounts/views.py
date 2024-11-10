from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    def post(self, request):
        serializer= RegisterSerializer(data= request.data)
        if serializer.is_valid():
            user= serializer.save()
            return Response({"message": "User created successfully", "data": serializer.data}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        data= request.data
        username= data.get('username')
        password= data.get('password')
        user= User.objects.filter(username = username).first()
        if user and user.check_password(password):  
            refresh= RefreshToken.for_user(user)
            return Response({
                "access token": str(refresh.access_token),
                "refresh token": str(refresh)
                })
        return Response({"message": "Invalid Credentialis"}, status= status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self, request):
        serializer= RegisterSerializer(request.user)
        return Response(serializer.data)