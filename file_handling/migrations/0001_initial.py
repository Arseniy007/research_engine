# Generated by Django 4.2.3 on 2024-01-10 20:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import file_handling.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookshelf', '0001_initial'),
        ('paper_work', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to=file_handling.models.source_saving_path)),
                ('source', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='file', to='bookshelf.source')),
            ],
        ),
        migrations.CreateModel(
            name='PaperFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saving_time', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=file_handling.models.paper_saving_path)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='paper_work.paper')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
