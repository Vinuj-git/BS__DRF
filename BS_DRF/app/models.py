from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


USER_TYPE_CHOICES = (
    ("user", "USER"),
    ("librarian", "LIBRARIAN")
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=30,
        choices = USER_TYPE_CHOICES,
        default = 'user')


class Book(models.Model):  
    name = models.CharField(max_length=20)  
    auther = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.name
    

BOOK_STATUS_CHOICES = (
    ("issued", "ISSUED"),
    ("returned", "RETURNED")
)


class UserToBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_date = models.DateTimeField(blank=False,null=False)
    user_price = models.DecimalField(max_digits=6, decimal_places=2)
    returned_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=30,
        choices = BOOK_STATUS_CHOICES,
        default = 'issued')
    
    def __str__(self):
        return f"{self.book} - {self.user}"