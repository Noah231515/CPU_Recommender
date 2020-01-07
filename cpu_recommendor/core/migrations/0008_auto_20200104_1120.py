# Generated by Django 2.2.3 on 2020-01-04 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200103_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpu',
            name='blend_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cpu',
            name='gaming_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cpu',
            name='productivity_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cpu',
            name='value_score',
            field=models.FloatField(default=0),
        ),
    ]
