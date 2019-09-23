import logging

from typing import Iterable, NamedTuple
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.text import capfirst
from io import BytesIO
from time import strftime
from xlsxwriter import Workbook

from parcours_imi.models import Master, UserParcours


logger = logging.getLogger(__name__)


BASE_FIELD_NAMES = [
    'first_name',
    'last_name',
    'email',
    'master',
    'option',
]

BASE_FIELD_NAMES = [
    'Prénom',
    'Nom',
    'Email',
    'Master',
    'Option',
]


def user_parcours_export_view(request):
    file_response = HttpResponse(content=user_parcours_export())

    file_response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    timestamp = strftime('%Y-%m-%d_%H_%M_%S')
    file_response['Content-Disposition'] = f'attachment; filename="my3a_export_{timestamp}.xlsx"'

    return file_response

def build_course_row(courses, prefix):
    return {
        f"{prefix}{i}": course.name
        for i, course in enumerate(courses)
    }

def user_parcours_export():
    all_parcours = UserParcours.objects.all()

    logger.info(f'Exporting {len(all_parcours)} students')

    if all_parcours:
        max_main_courses = max([
            parcours.course_choice.main_courses.count() if parcours.course_choice else 0
            for parcours in all_parcours
        ])

        max_option_courses = max([
            parcours.course_choice.option_courses.count() if parcours.course_choice else 0
            for parcours in all_parcours
        ])
    else:
        max_main_courses = 0
        max_option_courses = 0

    field_names = {
        'first_name': 'Prénom',
        'last_name': 'Nom',
        'email': 'Email',
        'master': 'Master',
        'option': 'Option',
    }

    for i in range(max_main_courses):
        field_names[f'master_course_{i}'] = f'Cours master {i + 1}'

    for i in range(max_option_courses):
        field_names[f'option_course_{i}'] = f'Cours supplémentaire {i + 1}'

    output = BytesIO()

    with Workbook(output) as workbook:
        worksheet = workbook.add_worksheet()

        worksheet.write_row(0, 0, list(field_names.values()))
        for row_idx, parcours in enumerate(all_parcours, 1):
            row = dict(
                first_name=parcours.user.first_name,
                last_name=parcours.user.last_name,
                email=parcours.user.email,
                master=parcours.master.short_name,
                option=parcours.get_option_display(),
            )

            if parcours.course_choice and parcours.course_choice.submitted:
                row.update(build_course_row(parcours.course_choice.main_courses.all(), prefix='master_course_'))
                row.update(build_course_row(parcours.course_choice.option_courses.all(), prefix='option_course_'))

            worksheet.write_row(row_idx, 0, [row.get(field_name) for field_name in field_names.keys()])

    output.seek(0)
    return output
