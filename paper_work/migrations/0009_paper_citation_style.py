# Generated by Django 4.2.3 on 2024-02-17 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper_work', '0008_alter_bibliography_apa_alter_bibliography_mla'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='citation_style',
            field=models.CharField(choices=[('APA', 'APA'), ('MLA', 'MLA')], default='APA', max_length=3),
            preserve_default=False,
        ),
    ]