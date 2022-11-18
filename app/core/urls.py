from django.urls import path
from .views import ItemView, OrderView

urlpatterns = [
    path("item/<int:item_id>", ItemView.as_view(), name='item-detail'),
    path("order/<int:order_id>", OrderView.as_view(), name='order-detail'),
]
