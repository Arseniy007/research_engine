# Generated by Django 4.2.3 on 2024-02-18 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_handling', '0004_alter_paperfile_version_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperfile',
            name='file_extension',
            field=models.CharField(default='pdf', max_length=5),
            preserve_default=False,
        ),
    ]
