from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from messaging.models import Conversation


class Master(models.Model):
    name = models.CharField(max_length=120, verbose_name='Nom')
    short_name = models.CharField(max_length=6, verbose_name='Nom court')
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=120, verbose_name='Nom')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, null=True)
    ECTS = models.FloatField(verbose_name='ECTS')
    semester = models.CharField(max_length=20, verbose_name='Semestre')
    location = models.CharField(max_length=120, blank=True, null=True)
    time = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'

    def __str__(self):
        return self.name


class UserCourseChoice(models.Model):
    main_courses = models.ManyToManyField(Course, related_name='main_courses', blank=True)
    option_courses = models.ManyToManyField(Course, related_name='option_courses', blank=True)

    comment = models.TextField(verbose_name='Commentaire', blank=True, null=True)

    submitted = models.BooleanField(verbose_name='Validé par l\'étudiant', default=False)


OPTIONS = [
    ('3A-ecole', '3A École'),
    ('3A-M2-PFE', '3A M2 Imbriqués - Option 1'),
    ('3A-M2-ECTS', '3A M2 Imbriqués - Option 2'),
]

OPTIONS_KEYS = [
    key
    for key, val in OPTIONS
]


class UserParcours(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parcours')

    master = models.ForeignKey(Master, on_delete=models.PROTECT)
    option = models.CharField(max_length=120, choices=OPTIONS, blank=True, null=True, default=None)

    course_choice = models.OneToOneField(
        UserCourseChoice,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        related_name='course_choice',
    )

    # conversation = models.ForeignKey(Conversation, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = 'Parcours étudiant'
        verbose_name_plural = 'Parcours étudiants'

    def __str__(self):
        return self.user.username
