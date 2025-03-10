from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task
from django.utils.timezone import now

@receiver(pre_save, sender=Task)
def update_timestamp(sender, instance, **kwargs):
    """Ensure `updated_at` is set on any changes."""
    print('signals got triggered...')
    instance.updated_at = now()
