from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property
from django.http import JsonResponse
from .utils import get_all_properties

# Create your views here.

@cache_page(60 * 15)
def property_list(request):
    properties = get_all_properties()
    
    property_data = [
        {
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': prop.price,
            'location': prop.location,
            'created_at': prop.created_at,
        }
        for prop in properties
    ]

    return JsonResponse({'properties': property_data})
