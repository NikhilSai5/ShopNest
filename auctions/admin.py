from django.contrib import admin
from .models import Listing
from .models import Bid
from .models import Watchlist


admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Watchlist)
