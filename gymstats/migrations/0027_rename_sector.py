# Generated by Django 4.1.7 on 2023-10-01 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("gymstats", "0026_crag_gym_name"),
    ]

    operations = [
        migrations.RenameModel('Sector', 'IndoorSector')
    ]
