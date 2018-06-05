from django.contrib.auth.models import User
from django.db import models


class Master(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    troisa_possible = models.BooleanField(default=1)

    def __str__(self):
        return self.name


class Course(models.Model):
    OPTIONS = (
        ('Mo', 'Lundi'),
        ('Tu', 'Mardi'),
        ('We', 'Mercredi'),
        ('Th', 'Jeudi'),
        ('Fr', 'Vendredi'),
    )
    master = models.ForeignKey(Master, related_name='courses', on_delete=models.CASCADE)
    # l'attribut obligatoire vaut 1 si le cours en question est obligatoire pour le master associé
    obligatoire = models.BooleanField(default=0)
    title = models.CharField(max_length=100)
    lat = models.FloatField()
    long = models.FloatField()
    ects = models.FloatField()
    semester = models.PositiveSmallIntegerField()
    days = models.CharField(max_length=2, choices=OPTIONS)
    duration = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class Option(models.Model):
    name = models.CharField(max_length=300)
    nb_cours = models.PositiveSmallIntegerField(default=0)
    nb_ects_cours = models.FloatField(default=0)
    nb_projet = models.PositiveSmallIntegerField(default=0)
    nb_ects_projet = models.FloatField(default=0)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    def default_option():
        return Option.objects.all()[0]

    def default_master():
        return Master.objects.all()[0]

    option = models.ForeignKey(Option, related_name='profiles', on_delete=models.CASCADE)
    master = models.ForeignKey(Master, related_name='profiles', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, related_name='profiles')

    def __unicode__(self):
        return self.user.username
