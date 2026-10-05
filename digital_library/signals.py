from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from digital_library.models import Reader, Shelf


@receiver(post_save, sender=Reader)
def create_default_shelves(sender, instance, created, raw, **kwargs):
    if raw:
        return
    if created:
        Shelf.objects.create(reader=instance, name="Want to read")
        Shelf.objects.create(reader=instance, name="Currently reading")
        Shelf.objects.create(reader=instance, name="Read")
        Shelf.objects.create(reader=instance, name="Did not finish")
