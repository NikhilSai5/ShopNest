from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.mainPage, name="mainpage"),
    path("signin/", views.SignInPage, name="signinpage"),
    path("Signup/", views.SignUpPage, name="signuppage"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sell/', views.create_listing, name='sell'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('category/<str:category>/',
         views.category_listings, name='category_listings'),
    path('listing/<int:listing_id>/', views.item_details, name='item_details'),
    path('close_auction/<int:listing_id>/',
         views.close_auction, name='close_auction'),
    path('toggle_watchlist/<int:listing_id>/',
         views.toggle_watchlist, name='toggle_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('bid_history/', views.bid_history, name='bid_history'),
]
