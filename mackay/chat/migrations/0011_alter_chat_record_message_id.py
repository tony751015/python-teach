# Generated by Django 5.0.6 on 2024-10-14 04:45

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0010_alter_chat_record_message_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chat_record",
            name="message_id",
            field=models.UUIDField(
                default=uuid.UUID("ee286583-d121-48cd-b252-413291bf255a"),
                editable=False,
            ),
        ),
    ]