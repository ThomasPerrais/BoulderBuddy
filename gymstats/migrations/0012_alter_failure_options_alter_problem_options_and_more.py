# Generated by Django 4.1.7 on 2023-04-04 16:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0011_alter_session_fear_alter_session_motivation_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="failure",
            options={"ordering": ["-session__date", "problem__grade"]},
        ),
        migrations.AlterModelOptions(
            name="problem",
            options={"ordering": ["-date_added"]},
        ),
        migrations.AlterModelOptions(
            name="session",
            options={"ordering": ["-date"]},
        ),
        migrations.AlterModelOptions(
            name="top",
            options={"ordering": ["-session__date", "problem__grade"]},
        ),
        migrations.AlterModelOptions(
            name="zone",
            options={"ordering": ["-session__date", "problem__grade"]},
        ),
    ]
