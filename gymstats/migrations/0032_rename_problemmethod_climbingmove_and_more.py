# Generated by Django 4.1.7 on 2023-10-08 16:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0031_rename_problem_indoorproblem"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ProblemMethod",
            new_name="ClimbingMove",
        ),
        migrations.RenameModel(
            old_name="ProblemType",
            new_name="WallAngle",
        ),
    ]
