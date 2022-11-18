from django.views.generic import DetailView
from core.models import Item, Order
from django.http import JsonResponse


# Create your views here.
class ItemView(DetailView):
    model = Item 
    context_object_name: str = 'item'
    pk_url_kwarg: str = 'item_id'
    template_name: str = 'core/item.html'


class OrderView(DetailView):
    model = Order 
    context_object_name: str = 'order'
    pk_url_kwarg: str = 'order_id'
    template_name: str = 'core/order.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_items"] = self.get_object().items.all()
        return context




