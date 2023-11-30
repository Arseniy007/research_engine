# Generated by Django 4.2.3 on 2023-11-30 19:27

import bookshelf.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('work_space', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(blank=True, max_length=70)),
                ('year', models.CharField(blank=True, max_length=5)),
                ('file', models.FileField(blank=True, upload_to=bookshelf.models.saving_path)),
                ('link', models.CharField(blank=True, max_length=40)),
                ('real_type', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to=settings.AUTH_USER_MODEL)),
                ('work_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='work_space.workspace')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bookshelf.source')),
                ('journal_title', models.CharField(max_length=50)),
                ('volume', models.CharField(max_length=10)),
                ('issue', models.CharField(max_length=10)),
                ('pages', models.CharField(max_length=20)),
                ('link_to_journal', models.CharField(blank=True, max_length=40)),
            ],
            bases=('bookshelf.source',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bookshelf.source')),
                ('publishing_house', models.CharField(max_length=20)),
            ],
            bases=('bookshelf.source',),
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bookshelf.source')),
                ('book_title', models.CharField(max_length=50)),
                ('book_author', models.CharField(max_length=70)),
                ('publishing_house', models.CharField(max_length=20)),
                ('edition', models.CharField(max_length=10)),
                ('pages', models.CharField(max_length=20)),
            ],
            bases=('bookshelf.source',),
        ),
        migrations.CreateModel(
            name='Webpage',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bookshelf.source')),
                ('website_title', models.CharField(max_length=50)),
                ('page_url', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=20)),
            ],
            bases=('bookshelf.source',),
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.IntegerField()),
                ('text', models.TextField()),
                ('apa', models.CharField(max_length=20)),
                ('mla', models.CharField(max_length=20)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='bookshelf.source')),
            ],
        ),
        migrations.CreateModel(
            name='Endnote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apa', models.CharField(max_length=50)),
                ('mla', models.CharField(max_length=50)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookshelf.source')),
            ],
        ),
    ]
