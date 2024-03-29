# Generated by Django 4.1.7 on 2023-04-01 10:31

from django.db import migrations, models
import gymstats.models


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0009_zone_top_failure"),
    ]

    operations = [
        migrations.AlterField(
            model_name="describable",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="describable"
            ),
        ),
        migrations.AlterField(
            model_name="problem",
            name="footwork",
            field=models.ManyToManyField(blank=True, to="gymstats.footwork"),
        ),
        migrations.AlterField(
            model_name="problem",
            name="hand_holds",
            field=models.ManyToManyField(blank=True, to="gymstats.handhold"),
        ),
        migrations.AlterField(
            model_name="problem",
            name="picture",
            field=models.ImageField(upload_to=gymstats.models.Climbable.upload_picture),
        ),
        migrations.AlterField(
            model_name="problem",
            name="problem_method",
            field=models.ManyToManyField(blank=True, to="gymstats.problemmethod"),
        ),
    ]
