# Generated by Django 4.1.3 on 2023-01-07 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_todo_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='todo_photos/'),
        ),
    ]
