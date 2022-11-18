from django.urls import path 
from .views import buyItemView, buyOrderView

urlpatterns = [
    path('buy-item/<int:pk>', buyItemView, name='checkout-item'),
    path('buy-order/<int:pk>', buyOrderView, name='checkout-order'),
]