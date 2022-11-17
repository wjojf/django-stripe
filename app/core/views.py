from django.views.generic import DetailView
from core.models import Item
from django.http import JsonResponse


# Create your views here.
class ItemView(DetailView):
    model = Item 
    context_object_name: str = 'item'
    pk_url_kwarg: str = 'item_id'
    template_name: str = 'core/item.html'





