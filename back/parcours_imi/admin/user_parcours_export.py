import codecs
import logging

from csv import DictWriter
from typing import Iterable, NamedTuple
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.text import capfirst
from io import StringIO
from time import strftime

from parcours_imi.models import Master, UserParcours


logger = logging.getLogger(__name__)


BASE_FIELD_NAMES = [
    'first_name',
    'last_name',
    'email',
    'master',
    'option',
]


def user_parcours_export_view(request):
    file_response = HttpResponse(content=user_parcours_export())

    file_response['Content-Type'] = 'text/csv'
    timestamp = strftime('%Y-%m-%d_%H_%M_%S')
    file_response['Content-Disposition'] = f'attachment; filename="export_{timestamp}.csv"'

    return file_response

def build_course_row(courses, prefix):
    return {
        f"{prefix}{i}": course.name
        for i, course in enumerate(courses, 1)
    }

def user_parcours_export():
    all_parcours = UserParcours.objects.all()

    logger.info(f'Exporting {len(all_parcours)} students')

    max_main_courses = max([
        parcours.course_choice.main_courses.count() if parcours.course_choice else 0
        for parcours in all_parcours
    ])

    max_option_courses = max([
        parcours.course_choice.option_courses.count() if parcours.course_choice else 0
        for parcours in all_parcours
    ])

    field_names = BASE_FIELD_NAMES + [
        f'master_course_{i + 1}'
        for i in range(max_main_courses)
    ] + [
        f'option_course_{i + 1}'
        for i in range(max_option_courses)
    ]

    csv_io = StringIO()
    writer = DictWriter(csv_io, fieldnames=field_names)

    writer.writeheader()
    for parcours in all_parcours:
        row = dict(
            first_name=parcours.user.first_name,
            last_name=parcours.user.last_name,
            email=parcours.user.email,
            master=parcours.master.short_name,
            option=parcours.option,
        )

        if parcours.course_choice and parcours.course_choice.submitted:
            row.update(build_course_row(parcours.course_choice.main_courses.all(), prefix='master_course_'))
            row.update(build_course_row(parcours.course_choice.option_courses.all(), prefix='option_course_'))

        writer.writerow(row)

    return csv_io.getvalue()
