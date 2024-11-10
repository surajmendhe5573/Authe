from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    def post(self, request):
        serializer= RegisterSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully", "data": serializer.data}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        data= request.data
        email= data.get('email')
        password= data.get('password')
        user= User.objects.filter(email = email).first()
        if user and user.check_password(password):  
            refresh= RefreshToken.for_user(user)
            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
                }, status= status.HTTP_200_OK)
        return Response({"message": "Invalid Credentials"}, status= status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request):
        serializer= RegisterSerializer(request.user)
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    