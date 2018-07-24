from django.contrib.auth.models import User
from django.db import models

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
    semester = models.PositiveSmallIntegerField(verbose_name='Semestre')
    location = models.CharField(max_length=120, blank=True, null=True)
    time = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'

    def __str__(self):
        return self.name


FORMULAS = [
    ('3A-ecole', '3A École'),
    ('3A-M2-PFE', '3A M2 Imbriqués - Option 1'),
    ('3A-M2-ECTS', '3A M2 Imbriqués - Option 2'),
]


class UserParcours(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parcours')

    master = models.ForeignKey(Master, on_delete=models.PROTECT)
    formula = models.CharField(max_length=120, choices=FORMULAS)
    courses = models.ManyToManyField(Course, related_name='courses', blank=True)
    coursesOption2 = models.ManyToManyField(Course, related_name='coursesOption2', blank=True)

    comment = models.TextField(verbose_name='Commentaire', blank=True)

    submitted = models.BooleanField(verbose_name='Validé par l\'étudiant', default=False)

    # conversation = models.ForeignKey(Conversation, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = 'Parcours étudiant'
        verbose_name_plural = 'Parcours étudiants'

    def __str__(self):
        return self.user.username
