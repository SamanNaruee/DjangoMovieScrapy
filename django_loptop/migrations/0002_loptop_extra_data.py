# Generated by Django 5.1.4 on 2025-01-01 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_loptop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loptop',
            name='extra_data',
            field=models.JSONField(default=dict),
        ),
    ]