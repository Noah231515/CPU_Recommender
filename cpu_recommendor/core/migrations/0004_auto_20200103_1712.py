# Generated by Django 2.2.3 on 2020-01-03 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_cpu_cores'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpu',
            name='base_clock',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cpu',
            name='boost_clock',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cpu',
            name='integrated_graphics',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='cpu',
            name='multhithreading',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cpu',
            name='tdp',
            field=models.IntegerField(default=0),
        ),
    ]
