from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # age = serializers.IntegerField(required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'age', 'phone_number', 'address', 'marital_status', 'is_active', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # email = validated_data.get('email')
        user = CustomUser.objects.create_user( password=password, **validated_data)
        return user
    
    # def validate_age(self, value):
    #     if value < 18:
    #         raise serializers.ValidationError("User must be at least 18 years old.")
    #     return value
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
   