# Generated by Django 5.0.6 on 2025-04-24 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linerobot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_linebot_track',
            name='category',
            field=models.TextField(blank=True, default='system'),
        ),
    ]
