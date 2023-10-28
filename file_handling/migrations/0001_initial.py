# Generated by Django 4.2.3 on 2023-10-28 18:46

from django.db import migrations, models
import django.db.models.deletion
import file_handling.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('paper_work', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaperVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saving_time', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=file_handling.models.user_directory_path)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paper_work.paper')),
            ],
        ),
    ]
