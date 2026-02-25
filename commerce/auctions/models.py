from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    author = models.ForeignKey(User,on_delete=models.CASCADE ,related_name="auctions")
    status = models.BooleanField(default=True)
    category = models.CharField(max_length=100,blank=True)
    time = models.TimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(default=timezone.now() + timedelta(days=3))
    url = models.URLField(blank=True)

class Bid(models.Model):
    auction = models.ForeignKey(AuctionListing,on_delete=models.CASCADE,related_name="bids")
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bids")
    price =models.DecimalField(max_digits=10,decimal_places=2)

class Comment(models.Model):
    auction = models.ForeignKey(AuctionListing,on_delete=models.CASCADE,related_name="comments")
    author= models.ForeignKey(User,on_delete=models.CASCADE ,related_name="comments")
    description=models.TextField(max_length=1000)

class Watchlist(models.Model):
    auction=models.ForeignKey(AuctionListing,on_delete=models.CASCADE,related_name="Watchlist")
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="Watchlist")



