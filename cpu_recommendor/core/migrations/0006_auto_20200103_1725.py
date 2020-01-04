# Generated by Django 2.2.3 on 2020-01-03 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200103_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='boost_clock',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='integrated_graphics',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='release_date',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
