from .permissions import LibrarianEditOrReadOnly
from .models import Book, Profile, UserToBook
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from app.serializers import BookSerializer, LoginSerializer, SignupSerializer, UserBookSerializer, UserProfileSerializer, UserToBookSerializer
import datetime


class SignupView(APIView):
    permission_classes = (AllowAny, )
    signup_serializer_class = SignupSerializer
    def post(self, request, format=None):
        signup_serializer = self.signup_serializer_class(data=request.data)
        signup_serializer.is_valid(raise_exception=True)
        user = signup_serializer.save()

        return Response({"message": "User registration completed successfully."}, status=status.HTTP_201_CREATED)
    

class LoginView(APIView):
    permission_classes = (AllowAny, )
    login_serializer_class = LoginSerializer
    user_profile_serializer_class = UserProfileSerializer
    def post(self, request, format=None):
        serializer = self.login_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.login()

        try:
            profile = Profile.objects.get(user_id=user.id)
        except Profile.DoesNotExist:
            return Response({"message": "User Profile does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = self.user_profile_serializer_class(profile)
        token = RefreshToken.for_user(user)
        
        jwt_access_token_lifetime =  settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        jwt_refresh_token_lifetime =  settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        data = {
          "refresh": str(token),
          "access": str(token.access_token),
          "access_token_life_time_in_seconds" : jwt_access_token_lifetime.total_seconds(),
          "refresh_token_life_time_in_seconds" : jwt_refresh_token_lifetime.total_seconds(),
        }
        user_profile_data = user_profile.data
        auth_user_data = user_profile_data.pop('user')
        user_profile_data.update(auth_user_data)
        data.update({ 'user_profile' : user_profile_data })
        return Response(data, status=status.HTTP_200_OK)
        
        
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [LibrarianEditOrReadOnly]


class BookSearchView(APIView):
    permission_classes = (LibrarianEditOrReadOnly,)
    def get(self, request, name):
        book = Book.objects.filter(name__icontains=name)
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class UserBookView(APIView):
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            return [LibrarianEditOrReadOnly()]
        return [permission() for permission in self.permission_classes]
    
    def get(self, request, format=None):
        user_book = UserToBook.objects.filter(user=request.user,status="issued")
        for obj in user_book:
            base_price = obj.book.price
            date = obj.issued_date.strftime( "%Y-%m-%d %H:%M:%S.%f")
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
            
            if (datetime.datetime.now() - date).days > 7:
                obj.user_price = (base_price) + 10*((datetime.datetime.now() - date).days - 7)
                obj.save()
                
        serializer = UserToBookSerializer(user_book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request, format=None):
        data=request.data
        book = Book.objects.get(id=request.data['book'])
        data['user_price'] = book.price
        serializer = UserBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)