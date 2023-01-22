from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category0 = models.CharField(max_length=50)
    def __str__(self):
        return self.category0




class Listing(models.Model):
   brand = models.CharField(max_length=30)
   model = models.CharField(max_length=30)
   description = models.CharField(max_length=300)
   imageUrl = models.CharField(max_length=1000)
   price = models.FloatField()
   isActive = models.BooleanField(default=True)
   owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
   category1 = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="catagory")
   watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingwatchlist")
   def __str__(self):
        return self.model

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_id")
    date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commentuser")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listinguser")
    comment = models.CharField(max_length=150)
    def __str__(self):
        return self.comment

class Bid(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="biduser")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="bidlisting")
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __float__(self):
        return self.bid      