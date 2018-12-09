import logging

from django.contrib import messages
from django.shortcuts import render, redirect

from parcours_imi.models import UserParcours
from parcours_imi.tasks import send_user_parcours_reset_email


logger = logging.getLogger(__name__)


def user_parcours_reset_view(request, object_id):
    try:
        user_parcours = UserParcours.objects.get(pk=object_id)
    except UserParcours.DoesNotExist:
        raise Exception

    user_parcours.option = None
    user_parcours.save()

    try:
        course_choice = user_parcours.course_choice
    except UserParcours.course_choice.RelatedObjectDoesNotExist:
        course_choice = None

    if course_choice:
        course_choice.delete()

    send_user_parcours_reset_email.delay(object_id)

    messages.success(request, 'Parcours réinitialisé avec succès.')
    return redirect('admin:parcours_imi_userparcours_change', object_id=object_id)
