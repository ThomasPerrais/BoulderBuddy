# Generated by Django 4.1.7 on 2023-11-01 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0038_nc1_indoorproblem_climbable"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="failure",
            options={"ordering": ["-session__date", "problem__climbable__grade"]},
        ),
        migrations.AlterModelOptions(
            name="indoorproblem",
            options={"ordering": ["-date_added", "climbable__grade"]},
        ),
        migrations.AlterModelOptions(
            name="outdoorproblem",
            options={"ordering": ["climbable__grade"]},
        ),
        migrations.AlterModelOptions(
            name="top",
            options={"ordering": ["-session__date", "problem__climbable__grade"]},
        ),
        migrations.AlterModelOptions(
            name="zone",
            options={"ordering": ["-session__date", "problem__climbable__grade"]},
        ),
        migrations.RemoveField(
            model_name="indoorproblem",
            name="climb_attr",
        ),
        migrations.RemoveField(
            model_name="indoorproblem",
            name="grade",
        ),
        migrations.RemoveField(
            model_name="indoorproblem",
            name="moves",
        ),
        migrations.RemoveField(
            model_name="indoorproblem",
            name="picture",
        ),
        migrations.RemoveField(
            model_name="indoorproblem",
            name="wall_angle",
        ),
        migrations.RemoveField(
            model_name="outdoorproblem",
            name="climb_attr",
        ),
        migrations.RemoveField(
            model_name="outdoorproblem",
            name="grade",
        ),
        migrations.RemoveField(
            model_name="outdoorproblem",
            name="moves",
        ),
        migrations.RemoveField(
            model_name="outdoorproblem",
            name="picture",
        ),
        migrations.RemoveField(
            model_name="outdoorproblem",
            name="wall_angle",
        ),
        migrations.AddField(
            model_name="outdoorproblem",
            name="climbable",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="gymstats.nc1",
            ),
        ),
        migrations.AlterField(
            model_name="indoorproblem",
            name="climbable",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="gymstats.nc1",
            ),
        ),
    ]
