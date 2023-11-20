# Generated by Django 4.2.3 on 2023-11-18 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0015_quote_in_text_citation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='in_text_citation',
        ),
        migrations.AddField(
            model_name='quote',
            name='apa_citation',
            field=models.CharField(default='ss', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='mla_citation',
            field=models.CharField(default='www', max_length=20),
            preserve_default=False,
        ),
    ]