# Generated by Django 2.2.3 on 2020-01-03 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cpu',
            old_name='multithread_score',
            new_name='multithreaded_score',
        ),
    ]