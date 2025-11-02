from .models import Property
from django.core.cache import cache
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

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

def get_redis_cache_metrics():
    try:
        # get redis connection via django redis
        redis_conn = get_redis_connection('default')

        # get redis info command output
        info = redis_conn.info()

        # extract cache stats
        stats = info.get('stats', {})
        keyspace_hits = stats.get('keyspace_hits', 0)
        keyspace_misses = stats.get('keyspace_misses', 0)

        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        if total_requests > 0:
            hit_ratio = keyspace_hits / total_requests
            hit_ratio_percentage = hit_ratio * 100
        else:
            hit_ratio = 0.0
            hit_ratio_percentage = 0.0

        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total': total_requests,
            'hit_ratio': hit_ratio,
            'hit_ratio_percentage': hit_ratio_percentage,
        }

        logger.info(
            f"Redis Cache Metrics: "
            f"{metrics['hit_ratio_percentage']}% hit ratio "
            f"({metrics['keyspace_hits']} hits, {metrics['keyspace_misses']} misses) - "
        )

        return metrics
    
    except Exception as e:
        logger.error(f"Error getting Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0.0,
            'hit_ratio_percentage': 0.0,
        }