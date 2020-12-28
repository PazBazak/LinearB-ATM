from django.contrib import admin
from .models import Bill, Coin, Currency

# Register your models here.
admin.site.register(Bill)
admin.site.register(Coin)
admin.site.register(Currency)
