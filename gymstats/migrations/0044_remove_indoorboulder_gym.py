# Generated by Django 4.1.7 on 2023-11-01 19:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0043_alter_indoorboulder_climbable"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="indoorboulder",
            name="gym",
        ),
    ]
