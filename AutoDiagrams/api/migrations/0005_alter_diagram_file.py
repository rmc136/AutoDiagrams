# Generated by Django 3.2.8 on 2024-09-03 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_diagram_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagram',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='yaml_files/'),
        ),
    ]