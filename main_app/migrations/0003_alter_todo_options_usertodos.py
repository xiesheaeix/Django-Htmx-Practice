# Generated by Django 4.1.3 on 2023-01-07 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_todo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': [django.db.models.functions.text.Lower('description')]},
        ),
        migrations.CreateModel(
            name='UserTodos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField()),
                ('todo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.todo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
