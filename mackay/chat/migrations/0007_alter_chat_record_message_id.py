# Generated by Django 5.0.6 on 2024-10-02 07:06

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_chat_record_message_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat_record',
            name='message_id',
            field=models.UUIDField(default=uuid.UUID('1ad2d478-e00b-4b13-8c17-ba79d26d5f5f'), editable=False),
        ),
    ]