# Generated by Django 4.1.7 on 2023-11-01 18:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0041_rename_indoorproblem_indoorboulder_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="climbable",
            name="climb_type",
            field=models.ManyToManyField(blank=True, to="gymstats.climbtype"),
        ),
    ]
