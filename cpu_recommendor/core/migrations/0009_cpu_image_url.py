# Generated by Django 2.2.3 on 2020-01-22 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200104_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpu',
            name='image_url',
            field=models.URLField(default=''),
        ),
    ]
