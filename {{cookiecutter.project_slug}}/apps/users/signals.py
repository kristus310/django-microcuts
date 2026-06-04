from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile


User = get_user_model()


@receiver(post_delete, sender=UserProfile)
def delete_avatar_on_profile_delete(sender, instance, **kwargs):
    if instance.avatar:
        instance.avatar.storage.delete(instance.avatar.name)


@receiver(pre_save, sender=UserProfile)
def delete_old_avatar_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = UserProfile.objects.get(pk=instance.pk)
    except UserProfile.DoesNotExist:
        return
    if old.avatar and old.avatar != instance.avatar:
        old.avatar.storage.delete(old.avatar.name)


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)