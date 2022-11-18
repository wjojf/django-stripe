from .payment_api import StripePaymentAPI
from django.http import JsonResponse
from django.views import View
from core.models import Item



# Create your views here.
def buyItemView(request, pk):
    try:
        django_instance = Item.objects.get(pk=pk)
    except Exception as e:
        return JsonResponse({
            "error": e
        }, status=404)
    
    api_client = StripePaymentAPI()
    session = api_client.create_session_id(django_instance)
    status = 200 if session else 400


    return JsonResponse({"data": session, "meta": None}, status=status)
    
   