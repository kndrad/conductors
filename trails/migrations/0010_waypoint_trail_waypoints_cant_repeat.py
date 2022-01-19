# Generated by Django 4.0 on 2022-01-19 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trails', '0009_alter_waypoint_trail'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='waypoint',
            constraint=models.UniqueConstraint(fields=('trail_id', 'name'), name='trail_waypoints_cant_repeat'),
        ),
    ]
