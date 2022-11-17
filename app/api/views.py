from django.http import JsonResponse

# Create your views here.
def buyItemView(request, pk):
    return JsonResponse({'test': True})