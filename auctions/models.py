from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    startingBid = models.IntegerField()
    price = models.IntegerField(default = 0)
    active = models.BooleanField(default = True)
    description = models.TextField(max_length=2000, default="no description",)
    imageURL = models.CharField(max_length=128, blank = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name="listings", null = True)
    owner = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    user = models.CharField(max_length=64)
    body = models.TextField(max_length=2000)
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user}: {self.body}"

class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watching")

    
class Bids(models.Model):
    title = models.CharField(max_length=64)
    current = models.IntegerField(default=0)
    number = models.IntegerField(default = 0)
    owner = models.CharField(max_length=64)

    def __str__(self):
        return f"bids of {self.title}"

