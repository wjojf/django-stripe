from django.urls import path 
from .views import buyItemView

urlpatterns = [
    path('buy/<int:pk>', buyItemView.as_view(), name='buy-item'),
]