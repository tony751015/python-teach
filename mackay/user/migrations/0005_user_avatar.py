# Generated by Django 5.0.6 on 2024-10-23 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_alter_user_account_alter_user_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.TextField(blank=True, default=""),
        ),
    ]