# Generated by Django 5.0.6 on 2024-06-08 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]