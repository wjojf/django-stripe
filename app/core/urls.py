from django.urls import path
from .views import ItemView

urlpatterns = [
    path("item/<int:item_id>", ItemView.as_view(), name='home'),
]
