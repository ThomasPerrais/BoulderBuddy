# Generated by Django 4.1.7 on 2023-10-08 16:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0030_outdoorsector_notes"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Problem",
            new_name="IndoorProblem",
        ),
    ]
