import codecs
import logging

from csv import DictReader
from typing import Iterable, NamedTuple
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.text import capfirst

from parcours_imi.models import Master, UserParcours


logger = logging.getLogger(__name__)


class UserParcoursImportEntry(NamedTuple):
    username: str
    email: str
    first_name: str
    last_name: str
    master: str


class UserParcoursImportForm(forms.Form):
    file = forms.FileField(label='Fichier CSV')


def user_parcours_import_view(request):
    if request.method == 'GET' and request.GET.get('download_example'):
        file_response = HttpResponse(
            content=(
                'username,email,first_name,last_name,master\n'
                'louis.trezzini,louis.trezzini@eleves.enpc.fr,Louis,Trezzini,MVA\n'
                'clement.riu,clement.riu@eleves.enpc.fr,Clément,Riu,MVA\n'
            ),
        )

        file_response['Content-Type'] = 'text/csv'
        file_response['Content-Disposition'] = 'attachment; filename="example_import.csv"'

        return file_response

    if request.method == 'POST':
        form = UserParcoursImportForm(request.POST, request.FILES)

        if form.is_valid():
            csv_reader = DictReader(codecs.iterdecode(request.FILES['file'], 'utf-8'))

            students_to_import = [
                UserParcoursImportEntry(**row)
                for row in csv_reader
            ]

            user_parcours_import(students_to_import)

            messages.success(request, 'Étudiants importés avec succès.')
            return redirect('admin:index')
    else:
        form = UserParcoursImportForm()

    opts = UserParcours._meta
    context = {
        'module_name': str(capfirst(opts.verbose_name_plural)),
        'opts': opts,
        'form': form,
    }

    return render(request, 'admin/user_parcours_import.html', context)

def user_parcours_import(students_to_import: Iterable[UserParcoursImportEntry]):
    masters_map = {
        master.short_name: master
        for master in Master.objects.all()
    }

    logger.info(f'Importing {len(students_to_import)} students')
    for student in students_to_import:
        if student.master not in masters_map:
            continue

        user, created = User.objects.get_or_create(username=student.username)
        action_str = 'Creating' if created else 'Updating'
        logger.info(f'{action_str} student {student.username}')

        user.email = student.email
        user.first_name = student.first_name
        user.last_name = student.last_name

        master = masters_map[student.master]

        try:
            user.parcours.master = master
        except User.parcours.RelatedObjectDoesNotExist:
            user.parcours = UserParcours(
                user=user,
                master=master,
            )

        user.parcours.save()
        user.save()
