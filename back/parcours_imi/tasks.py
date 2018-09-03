import html2text
import logging
import os

from typing import Dict

from celery import shared_task
from templated_email import send_templated_mail

from parcours_imi.models import UserParcours


logger = logging.getLogger(__name__)

DEFAULT_FROM_EMAIL = '3a@enpc.fr'
DEFAULT_ADMIN_EMAIL_ADDRESS = 'till034+3A@gmail.com'


@shared_task
def send_option_confirmation_email(user_parcours_id: int):
    user_parcours = UserParcours.objects.get(pk=user_parcours_id)
    user = user_parcours.user

    logger.info(f'Sending option confirmation email for {user_parcours}')

    send_templated_mail(
        template_name='option_confirmation',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email, DEFAULT_ADMIN_EMAIL_ADDRESS],
        context=dict(
            user=user_parcours.user,
            user_parcours=user_parcours,
        ),
    )

@shared_task
def send_courses_validation_email(user_parcours_id: int, parcours_validation_data):
    user_parcours = UserParcours.objects.get(pk=user_parcours_id)
    user = user_parcours.user

    logger.info(f'Sending courses validation email for {user_parcours}')

    send_templated_mail(
        template_name='courses_validation',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email, DEFAULT_ADMIN_EMAIL_ADDRESS],
        context=dict(
            user=user_parcours.user,
            user_parcours=user_parcours,
            parcours_validation_data=parcours_validation_data,
        ),
    )
