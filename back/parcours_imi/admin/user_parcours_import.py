import codecs
import logging

from csv import DictReader
from typing import Iterable, NamedTuple
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from parcours_imi.models import Master, UserParcours


logger = logging.getLogger(__name__)


class UserParcoursImportEntry(NamedTuple):
    username: str
    email: str
    first_name: str
    last_name: str
    master: str


class UserParcoursImportForm(forms.Form):
    pass


def user_parcours_import_view(request):
    if request.method == 'POST':
        form = UserParcoursImportForm(request.POST, request.FILES)

        if form.is_valid():
            csv_reader = DictReader(codecs.iterdecode(request.FILES['file'], 'utf-8'))

            students_to_import = [
                UserParcoursImportEntry(**row)
                for row in csv_reader
            ]

            user_parcours_import(students_to_import)

            return HttpResponseRedirect('/')
    else:
        form = UserParcoursImportForm()

    return render(request, 'toto.html', dict(form=form))

def user_parcours_import(students_to_import: Iterable[UserParcoursImportEntry]):
    masters_map = {
        master.short_name: master
        for master in Master.objects.all()
    }

    logger.info(f'Importing {len(students_to_import)} students')
    for student in students_to_import:
        user, created = User.objects.get_or_create(username=student.username)
        action_str = 'Creating' if created else 'Updating'
        logger.info(f'{action_str} student {student.username}')

        user.email = student.email
        user.first_name = student.first_name
        user.last_name = student.last_name

        try:
            user.parcours.master = student.master
        except User.parcours.RelatedObjectDoesNotExist:
            user.parcours = UserParcours(
                user=user,
                master=masters_map[student.master],
            )

        user.parcours.save()
        user.save()



