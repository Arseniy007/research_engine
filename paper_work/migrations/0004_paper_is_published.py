# Generated by Django 4.2.3 on 2023-10-29 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper_work', '0003_paper_is_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
