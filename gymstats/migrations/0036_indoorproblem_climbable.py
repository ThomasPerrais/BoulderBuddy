# Generated by Django 4.1.7 on 2023-11-01 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0035_newclimbable"),
    ]

    operations = [
        migrations.AddField(
            model_name="indoorproblem",
            name="climbable",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="specific",
                to="gymstats.newclimbable",
            ),
        ),
    ]
