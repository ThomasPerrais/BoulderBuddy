# Generated by Django 4.1.7 on 2023-09-02 18:01

from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0024_remove_climber_mail"),
    ]

    operations = [
        migrations.CreateModel(
            name="IntervalStatistics",
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
                ("interval_id", models.IntegerField()),
                ("year", models.IntegerField()),
                (
                    "interval",
                    models.IntegerField(
                        choices=[(1, "Week"), (2, "Month"), (3, "Year")]
                    ),
                ),
                ("args", picklefield.fields.PickledObjectField(editable=False)),
                (
                    "climber",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="past_statistics",
                        to="gymstats.climber",
                    ),
                ),
            ],
        ),
    ]
