# Generated by Django 5.1.4 on 2025-01-07 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_loptop', '0011_phones'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptop',
            name='product_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phones',
            name='product_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]