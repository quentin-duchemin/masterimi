import os
from celery import shared_task

from parcours_imi.models import UserParcours

@shared_task
def send_option_validation_email(user_parcours_id: int):
    user_parcours = UserParcours.objects.get(pk=user_parcours_id)

    print(f"Handling option validation for {user_parcours} in {os.getpid()}")

@shared_task
def send_courses_validation_email(user_parcours_id: int):
    user_parcours = UserParcours.objects.get(pk=user_parcours_id)

    print(f"Handling courses validation for {user_parcours} in {os.getpid()}")
