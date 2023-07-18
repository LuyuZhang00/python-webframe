from django.contrib import admin
from django.utils.safestring import mark_safe
from . import models

class AuctionModelAdmin(admin.ModelAdmin):

    def cover(self, *args, **kwargs):
        return mark_safe("<a href='{0}'>{0}</a>".format(self.cover))

    list_display = ['title', cover, ]


admin.site.register(models.Auction, AuctionModelAdmin)


class AuctionItemModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'cover', 'auction', 'status']


admin.site.register(models.AuctionItem, AuctionItemModelAdmin)

admin.site.register(models.AuctionItemImage)


class AuctionItemDetailModelAdmin(admin.ModelAdmin):
    list_display = ['item', 'key', 'value']


admin.site.register(models.AuctionItemDetail, AuctionItemDetailModelAdmin)



admin.site.register(models.DepositRecord)