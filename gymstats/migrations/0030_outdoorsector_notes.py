# Generated by Django 4.1.7 on 2023-10-01 11:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0029_orientation_outdoorsector"),
    ]

    operations = [
        migrations.AddField(
            model_name="outdoorsector",
            name="notes",
            field=models.CharField(default="", max_length=1000),
            preserve_default=False,
        ),
    ]