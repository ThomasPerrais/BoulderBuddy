# Generated by Django 4.1.7 on 2023-11-01 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0039_alter_failure_options_alter_indoorproblem_options_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="NC1",
            new_name="Climbable",
        ),
        migrations.CreateModel(
            name="Crux",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("notes", models.CharField(max_length=1000)),
                (
                    "climb_attr",
                    models.ManyToManyField(blank=True, to="gymstats.climbattribute"),
                ),
                (
                    "climb_move",
                    models.ManyToManyField(blank=True, to="gymstats.climbingmove"),
                ),
                (
                    "climbable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cruxes",
                        to="gymstats.climbable",
                    ),
                ),
                (
                    "footwork",
                    models.ManyToManyField(blank=True, to="gymstats.footwork"),
                ),
                (
                    "hand_holds",
                    models.ManyToManyField(blank=True, to="gymstats.handhold"),
                ),
                (
                    "wall_angle",
                    models.ManyToManyField(blank=True, to="gymstats.wallangle"),
                ),
            ],
        ),
    ]