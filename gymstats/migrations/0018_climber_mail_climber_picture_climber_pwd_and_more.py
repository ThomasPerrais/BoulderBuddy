# Generated by Django 4.1.7 on 2023-06-14 10:19

from django.db import migrations, models
import django.db.models.deletion
import gymstats.models


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0017_ric"),
    ]

    operations = [
        migrations.AddField(
            model_name="climber",
            name="mail",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="climber",
            name="picture",
            field=models.ImageField(
                blank=True, upload_to=gymstats.models.Climber.upload_picture
            ),
        ),
        migrations.AddField(
            model_name="climber",
            name="pwd",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name="climber",
            name="stats_preference",
            field=models.IntegerField(
                choices=[(1, "Week"), (2, "Month"), (3, "Year"), (4, "All Time")],
                default=1,
            ),
        ),
        migrations.AddField(
            model_name="climber",
            name="week_hard_boulder_target",
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name="climber",
            name="week_hour_target",
            field=models.IntegerField(default=3),
        ),
        migrations.CreateModel(
            name="HardBoulderThreshold",
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
                ("grade_threshold", models.CharField(max_length=10)),
                (
                    "climber",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hard_boulders",
                        to="gymstats.climber",
                    ),
                ),
                (
                    "gym",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="gymstats.gym"
                    ),
                ),
            ],
        ),
    ]
