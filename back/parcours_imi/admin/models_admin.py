from django.contrib import admin

from parcours_imi.models import AttributeConstraint, Course, Master, UserParcours


@admin.register(AttributeConstraint)
class AttributeConstraintAdmin(admin.ModelAdmin):
    pass


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

    change_list_template = "admin/user_parcours_change_list.html"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
