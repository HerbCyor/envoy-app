# Generated by Django 5.0.2 on 2024-02-08 15:05

import django.db.models.deletion
import geolocation.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_calls', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('input_file', models.FileField(upload_to=geolocation.models.user_directory_path)),
                ('output_file', models.FileField(upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]