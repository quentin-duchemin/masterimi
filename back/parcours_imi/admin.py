import logging

from typing import NamedTuple
from django.contrib import admin
from django.contrib.auth.models import User

from parcours_imi.models import Course, Master, UserParcours


logger = logging.getLogger(__name__)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    pass


@admin.register(UserParcours)
class UserParcoursAdmin(admin.ModelAdmin):
    readonly_fields = ["user"]
    exclude = ["course_choice"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserParcoursImportEntry(NamedTuple):
    username: str
    email: str
    first_name: str
    last_name: str
    master: str

def user_parcours_import_view(request):
    students_to_import = [
        UserParcoursImportEntry(
            'louis.trezzini',
            'louis.trezzini@eleves.enpc.fr',
            'Louis',
            'Trezzini',
            'MVA',
        )
    ]

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



