from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.user.username


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.URLField()
    category_choices = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('footwear', 'Footwear'),
        ('home_and_furniture', 'Home and Furniture'),
        ('antique', 'Antique'),
    ]
    category = models.CharField(max_length=20, choices=category_choices)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_listing')
    current_highest_bid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    highest_bidder = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_winning_bid = models.BooleanField(default=False)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"{self.user.username}'s Watchlist - {self.listing.title}"
