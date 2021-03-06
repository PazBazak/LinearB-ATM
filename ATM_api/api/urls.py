from django.urls import path, include
from rest_framework import routers
from .views import CoinViewSet, BillViewSet, CurrencyViewSet, show_inventory, withdrawal

router = routers.DefaultRouter()

router.register('bills', BillViewSet)
router.register('coins', CoinViewSet)
router.register('currencies', CurrencyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('atm/inventory/', show_inventory),
    path('atm/withdrawal/', withdrawal),
]
