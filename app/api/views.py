from .payment_api import StripePaymentAPI
from django.http import JsonResponse
from django.views import View
from core.models import Item, Order


# Create your views here.
def buyItemView(request, pk):
    try:
        django_instance = Item.objects.get(pk=pk)
    except Exception as e:
        return JsonResponse({
            "error": e
        }, status=404)
    
    api_client = StripePaymentAPI()
    session = api_client.create_item_session_id(django_instance)
    status = 200 if session else 400

    return JsonResponse({"data": session, "meta": None}, status=status)


def buyOrderView(request, pk):
    try:
        django_instance = Order.objects.get(pk=pk)
    except Exception as e:
        return JsonResponse({
            "data": None,
            "meta": "Could not find Order with id {pk}"
        }, status=404)
    
    api_client = StripePaymentAPI()
    session = api_client.create_order_session_id(django_instance)
    status_code = 200 if session else 400

    meta = "Error generating checkout session" if status_code == 400 else None  
    
    return JsonResponse({
        "data": session,
        "meta": meta
    }, status=status_code)