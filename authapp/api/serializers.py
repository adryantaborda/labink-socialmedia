from rest_framework import serializers
from authapp.models import User
from django.contrib.auth import authenticate,login
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','bio','profile_picture']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            gender=validated_data['gender'],
            birthday=validated_data['birthday'],
        )

        return user

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username','password']

    def validate(self,validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = authenticate(username=username,password=password)

        if user is None:
            raise ValidationError("user doesn't exist.")
        
        elif not user.is_active:
            raise ValidationError("user isn't active.")
        
        validated_data['user'] = user

        return validated_data
    
    def perform_login(self):
        user = self.validated_data['user']
        print(f"Logging in user: {user}")
        login(self.context['request'], user)

class UserDeleteAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','password']
    
    def validate(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = authenticate(username = username, password = password)
        if not user:
            print("Invalid credentials:", username)
            raise ValidationError("Invalid credentials.")
        if not user.is_active:
            print("User is inactive:", username)
            raise ValidationError("User account is inactive.")  
        
        validated_data['user'] = user
        return validated_data
    
    def perform_delete(self):
        
        user = self.validated_data['user']
        print(user)
        user.delete()
        
        
