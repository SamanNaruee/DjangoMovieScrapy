# Generated by Django 5.1.4 on 2025-01-01 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_loptop', '0003_loptop_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loptop',
            name='extra_data',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
