# Generated by Django 5.0.6 on 2024-10-02 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_account_user_hashcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hashCode',
            field=models.TextField(blank=True, default=''),
        ),
    ]
