import html2text
import logging
import os

from typing import Dict

from celery import shared_task
from templated_email import send_templated_mail

from parcours_imi.models import UserParcours
from master_imi.settings import ADMIN_EMAIL


logger = logging.getLogger(__name__)

DEFAULT_FROM_EMAIL = 'my3a@enpc.org'


@shared_task(autoretry_for=(Exception,), retry_backoff=True)
def send_option_confirmation_email(user_parcours_id: int):
    user_parcours = UserParcours.objects.get(pk=user_parcours_id)
    user = user_parcours.user

    logger.info(f'Sending option confirmation email for {user_parcours}')

    send_templated_mail(
        template_name='option_confirmation',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email, ADMIN_EMAIL],
        context=dict(
            user=user,
            user_parcours=user_parcours,
        ),
    )

@shared_task(autoretry_for=(Exception,), retry_backoff=True)
def send_courses_validation_email(user_parcours_id: int, parcours_validation_data):
    user_parcours = UserParcours.objects.get(pk=user_parcours_id)
    user = user_parcours.user

    logger.info(f'Sending courses validation email for {user_parcours}')

    send_templated_mail(
        template_name='courses_validation',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email, ADMIN_EMAIL],
        context=dict(
            user=user,
            user_parcours=user_parcours,
            parcours_validation_data=parcours_validation_data,
        ),
    )

@shared_task(autoretry_for=(Exception,), retry_backoff=True)
def send_user_parcours_reset_email(user_parcours_id: int):
    user_parcours = UserParcours.objects.get(pk=user_parcours_id)
    user = user_parcours.user

    logger.info(f'Sending parcours reset email for {user_parcours}')

    send_templated_mail(
        template_name='user_parcours_reset',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email, ADMIN_EMAIL],
        context=dict(
            user=user,
            user_parcours=user_parcours,
        ),
    )
