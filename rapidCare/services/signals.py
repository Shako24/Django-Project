from django.db.models.signals import post_save
from django.dispatch import receiver
from userAuth.models import CustomUser
from services.models import Cart


@receiver(post_save, sender=CustomUser)
def new_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
