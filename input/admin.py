from django.contrib import admin
from .models import Donor, Donation, Item, Business, ClothingType, FundType, Clothing, Food, Fund, GiftCard, Miscellaneous
# Register your models here.
admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(Item)
admin.site.register(Business)
admin.site.register(ClothingType)
admin.site.register(FundType)
admin.site.register(Clothing)
admin.site.register(Food)
admin.site.register(Fund)
admin.site.register(GiftCard)
admin.site.register(Miscellaneous)
