# Generated by Django 4.2.3 on 2023-11-04 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0005_remove_editedbook_authors_remove_editedbook_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='multiple_authors',
        ),
    ]
