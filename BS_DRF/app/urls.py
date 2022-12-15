from django.urls import path, include

from . import views

from .views import BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'book', BookViewSet)



urlpatterns = [

    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('books/<str:name>',views.BookSearchView.as_view(),name='books-search'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('issue-book/',views.UserBookView.as_view(),name='issue-book'),
    path('', include(router.urls)),
]