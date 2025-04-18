# Generated by Django 5.0.6 on 2025-04-17 08:21

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0021_alter_chat_record_message_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chat_record",
            name="message_id",
            field=models.UUIDField(
                default=uuid.UUID("03978e4a-895d-4b6c-8e63-323491d0f872"),
                editable=False,
            ),
        ),
    ]
