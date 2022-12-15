from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import Profile, Book, UserToBook
from django.db.models import Q
from django.contrib import auth

class SignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, min_length=3, max_length=80)
    last_name = serializers.CharField(required=True, min_length=3, max_length=80)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True, min_length=8)
    user_type = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'user_type')


    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        confirm_password = validated_data.pop('confirm_password')
        auth_user = User.objects.create_user(**validated_data)
        user_profile_data = { 
            'user_type': user_type
        }
        user_profile = Profile.objects.create(user = auth_user, **user_profile_data)
        return auth_user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=5, max_length=64, write_only=True, required=True)
    password = serializers.CharField(min_length=6, max_length=64, write_only=True, required=True)

    def login(self, **kwargs):
        username = self.validated_data['username']
        password = self.validated_data['password']

        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        if not user:
            raise serializers.ValidationError({"message": ["No active account found with the given credentials."]})

        user = auth.authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError({"message": ["No active account found with the given credentials."]})
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ['first_name', 'last_name', 'username','email','is_active','date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['user', 'user_type',]
        
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class UserToBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    class Meta:
        model = UserToBook
        fields =  "__all__"


class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToBook
        fields =  "__all__"