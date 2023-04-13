# Generated by Django 4.1.7 on 2023-03-30 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0003_zone_rename_success_top_remove_problem_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="try",
            name="climber",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                to="gymstats.climber",
            ),
            preserve_default=False,
        ),
    ]
