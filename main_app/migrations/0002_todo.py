# Generated by Django 4.1.3 on 2023-01-05 23:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=128, unique=True)),
                ('users', models.ManyToManyField(related_name='todos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
