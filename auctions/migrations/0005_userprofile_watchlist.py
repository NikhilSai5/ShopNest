# Generated by Django 4.2.5 on 2023-11-21 08:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_rename_current_bidding_listing_current_highest_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True, related_name="watchlist", to="auctions.listing"
            ),
        ),
    ]
