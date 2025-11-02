from .models import Property
from django.core.cache import cache

def get_all_properties():
    cached_properties = cache.get('all_properties')
    if cached_properties:
        return cached_properties

    properties = Property.objects.all()
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

    cache.set('all_properties', property_data, 3600)
    return property_data
