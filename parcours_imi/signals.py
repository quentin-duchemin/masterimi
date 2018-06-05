from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated


@receiver(cas_user_authenticated)
def log_cas_login(sender, **kwargs):
    print(kwargs)
