# Generated by Django 5.1.4 on 2025-01-01 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loptop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.PositiveBigIntegerField()),
                ('brand', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('specs', models.TextField()),
                ('image_url', models.URLField()),
                ('source_url', models.URLField()),
            ],
        ),
    ]
