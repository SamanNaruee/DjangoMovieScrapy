# Generated by Django 5.1.4 on 2025-01-05 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_loptop', '0005_alter_loptop_crawled_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loptop',
            name='image_url',
        ),
        migrations.AddField(
            model_name='loptop',
            name='image_urls',
            field=models.JSONField(blank=True, default=list),
        ),
    ]