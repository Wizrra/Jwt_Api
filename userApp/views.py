from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    # def create(self, request, *args, **kwargs):
    #   # age = serializer.validated_data.get('age')

    #   serializer = self.get_serializer(data=request.data)
    #   # if serializer.is_valid(raise_exception=True):
    #   #   headers = self.get_success_headers(serializer.data)
    #   #   return Response({"message": "User registered successfully", "user": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
    #   #   if serializer >= 18:
    #   #     return Response({"message": "User registered successfully", "user": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
    #   #   else:
    #   #      return Response({"error": "User must be at least 18 years old"}, status=status.HTTP_400_BAD_REQUEST)
    #   self.perform_create(serializer)
    #   return Response({"email": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User registered successfully", "user": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        ) 
        

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # 1. Validate the incoming data
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # 2. Find the user
        user = CustomUser.objects.filter(email=email).first()

        # 3. Check if user exists and password is correct
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)

        # 4. If something failed, return one error
        return Response(
            {"error": "Invalid email or password"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
class refreshTokenView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return Response({"access": new_access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        

class UserProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class greetingView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    age = serializers.IntegerField(required=True)

    def get(self, request):
        user = request.user
        user_age = user.age
        if user_age and user_age >= 18:
            return Response({"greetings": f"Hello {user.get_full_name()}",
                "legitimacy": "You are qualified to be a part of the ongoing event as you are old enough",
                "age": user.age,
                "eligible": True,
                "data": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "age": user.age,
                    "gender": user.gender,
                    "phone_number": user.phone_number,
                    "address": user.address,
                    "marital_status": user.marital_status}
                    }, status=status.HTTP_200_OK)
        return Response({"message": f"Sorry {user.first_name}, you must be at least 18 years old."}, status=status.HTTP_403_FORBIDDEN)