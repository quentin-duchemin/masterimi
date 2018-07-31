# Generated by Django 2.0.7 on 2018-07-29 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parcours_imi', '0003_auto_20180729_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourseChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, verbose_name='Commentaire')),
                ('submitted', models.BooleanField(default=False, verbose_name="Validé par l'étudiant")),
                ('main_courses', models.ManyToManyField(blank=True, related_name='courses', to='parcours_imi.Course')),
                ('option2_courses', models.ManyToManyField(blank=True, related_name='coursesOption2', to='parcours_imi.Course')),
            ],
        ),
        migrations.RemoveField(
            model_name='userparcours',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='userparcours',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='userparcours',
            name='coursesOption2',
        ),
        migrations.RemoveField(
            model_name='userparcours',
            name='submitted',
        ),
        migrations.AddField(
            model_name='userparcours',
            name='course_choice',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='course_choice', to='parcours_imi.UserCourseChoice'),
        ),
    ]