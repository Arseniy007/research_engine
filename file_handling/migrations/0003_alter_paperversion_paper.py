# Generated by Django 4.2.3 on 2023-10-29 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paper_work', '0003_paper_is_finished'),
        ('file_handling', '0002_paperversion_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperversion',
            name='paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='paper_work.paper'),
        ),
    ]
