from django.shortcuts import render, get_object_or_404
from .models import Watchlist
from .models import Listing, Bid, Watchlist
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .forms import RegistrationForm, UserLoginForm
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Listing
from django.shortcuts import get_object_or_404
from .models import Bid
from decimal import Decimal
from django.db.models import Max


def mainPage(request):
    user_name = request.user.username
    active_listings = Listing.objects.all()
    return render(request, "auctions/index.html", {'user_name': user_name, 'active_listings': active_listings, })


def SignUpPage(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = User.objects.create_user(
                username=username, email=email, password=password)

            login(request, user)

            return redirect('signinpage')
    else:
        form = RegistrationForm()

    return render(request, 'auctions/signup.html', {'form': form})


def SignInPage(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('mainpage')
    else:
        form = UserLoginForm()

    return render(request, 'auctions/signin.html', {'form': form})


@login_required
def create_listing(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_bid = request.POST.get('starting_bid')
        img = request.POST.get('img')
        category = request.POST.get('category')

        Listing.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            img=img,
            category=category,
            creator=request.user
        )

        return redirect('sell')

    return render(request, 'auctions/sell.html')


def category_listings(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, 'auctions/category_listings.html', {'listings': listings, 'category': category})


@login_required
def item_details(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    bids = listing.bids.all()
    num_bids = bids.count()
    highest_bid = listing.current_highest_bid
    highest_bidder = listing.highest_bidder

    if request.method == 'POST':
        new_bid = Decimal(request.POST.get('bid_amount'))
        if new_bid > listing.current_highest_bid and new_bid > listing.starting_bid:
            listing.current_highest_bid = new_bid
            listing.highest_bidder = request.user
            listing.save()

            Bid.objects.create(
                listing=listing, bidder=request.user, bid_amount=new_bid)

            bids = listing.bids.all()
            num_bids = bids.count()
            highest_bid = listing.current_highest_bid
            highest_bidder = listing.highest_bidder

    return render(request, 'auctions/item_details.html', {'listing': listing, 'bids': bids, 'num_bids': num_bids, 'highest_bid': highest_bid, 'highest_bidder': highest_bidder})


def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.user == listing.creator:
        listing.is_active = False
        listing.save()

        # Determine the winning bid
        winning_bid = listing.bids.order_by('-bid_amount').first()

        if winning_bid:
            winning_bid.is_winning_bid = True
            winning_bid.save()

            winner = winning_bid.bidder
            messages.success(
                request, f"The auction for '{listing.title}' has been closed. The winner is {winner.username}.")
        else:
            messages.warning(
                request, f"The auction for '{listing.title}' has been closed, but no bids were placed.")

    return redirect('item_details', listing_id=listing_id)


def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    # Check if the item is already in the user's watchlist
    watchlist_entry, created = Watchlist.objects.get_or_create(
        user=request.user, listing=listing)

    if created:
        messages.success(
            request, f"The item '{listing.title}' has been added to your Watchlist.")
    else:
        watchlist_entry.delete()
        messages.success(
            request, f"The item '{listing.title}' has been removed from your Watchlist.")

    return redirect('item_details', listing_id=listing_id)


def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)

    return render(request, 'auctions/watchlist.html', {'watchlist_items': watchlist_items})


def bid_history(request):
    user_winning_bids = Bid.objects.filter(
        bidder=request.user, is_winning_bid=True)
    return render(request, 'auctions/bid_history.html', {'user_winning_bids': user_winning_bids})
