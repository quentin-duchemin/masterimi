from django.contrib import admin

from parcours_imi.models import Course, Master, UserParcours


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
