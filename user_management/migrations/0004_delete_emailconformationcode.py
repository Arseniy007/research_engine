# Generated by Django 4.2.3 on 2023-12-25 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0003_emailconformationcode'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmailConformationCode',
        ),
    ]