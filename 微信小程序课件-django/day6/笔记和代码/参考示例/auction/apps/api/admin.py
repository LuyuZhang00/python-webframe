from django.contrib import admin

from . import models

admin.site.register(models.Auction)
admin.site.register(models.AuctionItem)
