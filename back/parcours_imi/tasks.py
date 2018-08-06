import html2text
import logging
import os

from typing import Dict

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import get_template

from parcours_imi.models import UserParcours


logger = logging.getLogger(__name__)

DEFAULT_FROM_EMAIL = '3a@enpc.fr'
DEFAULT_ADMIN_EMAIL_ADDRESS = 'till034+3A@gmail.com'


def send_template_email(
    subject: str,
    template_name: str,
    template_context: Dict,
    to_email: str,
):
    html_message = get_template(template_name).render(template_context)

    send_mail(
        subject,
        html2text.html2text(html_message),
        DEFAULT_FROM_EMAIL,
        [to_email],
        html_message=html_message,
    )


@shared_task
def send_option_validation_email(user_parcours_id: int):
    user_parcours = UserParcours.objects.get(pk=user_parcours_id)

    logger.debug(f"Sending option validation email for {user_parcours}")

    send_template_email(
        'Subject',
        'email/option_validation.html',
        {},
        user_parcours.user.email,
    )

@shared_task
def send_courses_validation_email(user_parcours_id: int):
    user_parcours = UserParcours.objects.get(pk=user_parcours_id)

    logger.debug(f"Sending courses validation email for {user_parcours}")

    send_template_email(
        'Subject',
        'email/courses_validation.html',
        {},
        user_parcours.user.email,
    )
