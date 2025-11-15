from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Currency


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_currency(sender, instance, created, **kwargs):
    """사용자 생성 시 Currency 자동 생성"""
    if created:
        Currency.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_currency(sender, instance, **kwargs):
    """사용자 저장 시 Currency도 저장"""
    if hasattr(instance, 'currency'):
        instance.currency.save()