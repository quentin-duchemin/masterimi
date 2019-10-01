import uuid

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import format_html

from parcours_imi.validators import ConstraintType, get_parcours_courses_rules_validation_data


class AttributeConstraint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')

    name = models.CharField(max_length=120, verbose_name='Nom')
    description = models.TextField(blank=True, verbose_name='Description')
    attribute = models.CharField(max_length=120, verbose_name='Attribut')
    min_value = models.FloatField(blank=True, null=True, verbose_name='Valeur minimale')
    max_value = models.FloatField(blank=True, null=True, verbose_name='Valeur maximale')

    class Meta:
        verbose_name = 'Contrainte'
        verbose_name_plural = 'Contraintes'

    def __str__(self):
        return self.name

class Option(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False, verbose_name='ID')

    name = models.CharField(max_length=120, verbose_name='Nom')

    def __str__(self):
        return self.name


class Master(models.Model):
    id = models.CharField(max_length=50, primary_key=True, editable=False, verbose_name='ID')

    name = models.CharField(max_length=120, verbose_name='Nom')
    short_name = models.CharField(max_length=10, verbose_name='Nom court')

    available_options = models.ManyToManyField(Option, related_name='available_options', blank=False)

    attribute_constraints = models.ManyToManyField(AttributeConstraint, related_name='attribute_constraints', blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')

    name = models.CharField(max_length=120, verbose_name='Nom')
    masters = models.ManyToManyField(Master, related_name='masters')
    ECTS = models.FloatField(verbose_name='ECTS')
    period = models.CharField(max_length=20, verbose_name='Période')
    location = models.CharField(max_length=120, blank=True, null=True, verbose_name='Lieu')
    time = models.CharField(max_length=120, blank=True, null=True, verbose_name='Horaires')

    attributes = JSONField(default=dict)

    class Meta:
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'

    def __str__(self):
        if not self.master:
            return self.name

        return f"({self.master.short_name} - {self.period}) {self.name}"

    @property
    def master(self):
        if not self.masters:
            return None

        return self.masters.first()


class UserCourseChoice(models.Model):
    main_courses = models.ManyToManyField(Course, related_name='main_courses', blank=True)
    option_courses = models.ManyToManyField(Course, related_name='option_courses', blank=True)

    comment = models.TextField(verbose_name='Commentaire', blank=True, null=True)

    submitted = models.BooleanField(verbose_name='Validé par l\'étudiant', default=False)

    class Meta:
        verbose_name = 'Choix de cours'
        verbose_name_plural = 'Choix de cours'

    def as_html(self):
        tag = '[Verrouillé]' if self.submitted else ''

        main_courses = self.main_courses.all()
        main_courses_names = ''.join([
            '<li>' + str(course) + '</li>'
            for course in main_courses
        ])

        option_courses = self.option_courses.all()
        option_courses_names = ''.join([
            '<li>' + str(course) + '</li>'
            for course in option_courses
        ])

        comment = '<br/> - ' + self.comment if self.comment else ' N/A'

        parcours_validation_data = get_parcours_courses_rules_validation_data(
            self.parcours,
            list(self.main_courses.all()),
            list(self.option_courses.all()),
        )
        validation_colors = {
            ConstraintType.VALID.value: 'green',
            ConstraintType.ERROR.value: 'red',
            ConstraintType.WARNING.value: 'orange',
        }
        validation_rules = ''.join([
            '<li style="color:{};">'.format(validation_colors[rule['type']]) + rule['full_message'] + '</li>'
            for rule in parcours_validation_data
        ])

        html_template = f'{tag} {len(main_courses)} cours (master) + {len(option_courses)} cours (option)<br/><br/>' \
            + f'Cours principaux :<br/><ul>{main_courses_names}</ul><br/><br/>' \
            + f'Cours pour la validation des 15 ECTS supplémentaires :<br/><ul>{option_courses_names}</ul><br/><br/>' \
            + f'Commentaire :{comment}<br/><br/>' \
            + f'Règles de validation :<br/><ul>{validation_rules}</ul>'

        return format_html(html_template)


class UserParcours(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parcours')

    master = models.ForeignKey(Master, on_delete=models.PROTECT)
    option = models.ForeignKey(Option, on_delete=models.PROTECT, blank=True, null=True, default=None)

    course_choice = models.OneToOneField(
        UserCourseChoice,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
        related_name='parcours',
    )

    class Meta:
        verbose_name = 'Parcours étudiant'
        verbose_name_plural = 'Parcours étudiants'

    def __str__(self):
        return self.user.username

    def get_option_display(self) -> str:
        if not self.option:
            return ""

        return self.option.name
