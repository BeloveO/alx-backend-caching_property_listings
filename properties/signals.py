from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from .models import Property


@receiver(post_save, sender=Property)
def clear_cache_on_save(sender, instance, **kwargs):
    # Clear cache when property is saved
    cache.delete('all_properties')

@receiver(post_delete, sender=Property)
def clear_cache_on_delete(sender, instance, **kwargs):
    # Clear cache when property is deleted
    cache.delete('all_properties')