# Generated by Django 4.2.3 on 2023-11-30 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_space', '0005_remove_invitation_invitation_type_spacesharecode'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SpaceShareCode',
            new_name='ShareSpaceCode',
        ),
    ]