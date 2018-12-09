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
    list_display = ['user', 'option', 'course_choice_submitted']

    fields = ['user', 'master', 'option', 'course_choice_html']
    readonly_fields = ['user', 'option', 'course_choice_html']

    change_list_template = 'admin/user_parcours_change_list.html'
    change_form_template = 'admin/user_parcours_change_form.html'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # ========================================================== #

    def course_choice_submitted(self, obj):
        if not obj.course_choice:
            return False

        return obj.course_choice.submitted

    course_choice_submitted.boolean = True
    course_choice_submitted.short_description = "Choix envoyés par l'étudiant"

    def course_choice_html(self, obj):
        if not obj.course_choice:
            return

        return obj.course_choice.as_html()

    course_choice_html.short_description = "Choix de cours"
