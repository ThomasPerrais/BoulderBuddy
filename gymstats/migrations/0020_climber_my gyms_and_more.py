# Generated by Django 4.1.7 on 2023-06-21 09:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "gymstats",
            "0019_rename_week_hard_boulder_target_climber_month_hard_boulder_target_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="climber",
            name="My Gyms",
            field=models.ManyToManyField(blank=True, to="gymstats.gym"),
        ),
        migrations.AlterField(
            model_name="climber",
            name="month_hard_boulder_target",
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name="climber",
            name="month_hour_target",
            field=models.IntegerField(default=10),
        ),
    ]