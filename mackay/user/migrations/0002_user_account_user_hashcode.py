# Generated by Django 5.0.6 on 2024-10-02 07:01

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='hashCode',
            field=models.UUIDField(default=uuid.UUID('0de5c76c-ab76-45e9-bce1-94d4b8edc4f8'), editable=False),
        ),
    ]