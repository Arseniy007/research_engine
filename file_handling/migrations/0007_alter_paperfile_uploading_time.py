# Generated by Django 4.2.3 on 2024-02-18 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_handling', '0006_paperfile_uploading_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperfile',
            name='uploading_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
