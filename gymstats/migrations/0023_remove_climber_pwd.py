# Generated by Django 4.1.7 on 2023-06-30 11:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0022_climber_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="climber",
            name="pwd",
        ),
    ]
