# Generated by Django 2.0.7 on 2018-07-17 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
        ('parcours_imi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userparcours',
            name='conversation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='messaging.Conversation'),
        ),
    ]
