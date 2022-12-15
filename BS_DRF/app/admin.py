from django.contrib import admin
from .models import Book, Profile, UserToBook

# Register your models here.

admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(UserToBook)