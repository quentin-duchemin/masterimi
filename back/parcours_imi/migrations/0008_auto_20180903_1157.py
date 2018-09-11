# Generated by Django 2.1 on 2018-09-03 09:57

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parcours_imi', '0007_auto_20180729_2301'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeConstraint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nom')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('attribute', models.CharField(max_length=120, verbose_name='Attribut')),
                ('min_value', models.FloatField(blank=True, null=True, verbose_name='Valeur minimale')),
                ('max_value', models.FloatField(blank=True, null=True, verbose_name='Valeur maximale')),
            ],
            options={
                'verbose_name': 'Contrainte',
                'verbose_name_plural': 'Contraintes',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='attributes',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='userparcours',
            name='course_choice',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='parcours', to='parcours_imi.UserCourseChoice'),
        ),
        migrations.AddField(
            model_name='master',
            name='attribute_constraints',
            field=models.ManyToManyField(blank=True, related_name='attribute_constraints', to='parcours_imi.AttributeConstraint'),
        ),
    ]