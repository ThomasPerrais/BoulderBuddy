# Generated by Django 4.1.7 on 2023-04-25 10:02

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0015_rename_location_gym_city_alter_sector_map"),
    ]

    operations = [
        migrations.AddField(
            model_name="gym",
            name="location",
            field=location_field.models.plain.PlainLocationField(
                default="-22.2876834,-49.1607606", max_length=63
            ),
            preserve_default=False,
        ),
    ]
