# Generated by Django 2.2.7 on 2019-11-28 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='user_score',
            field=models.FloatField(),
        ),
    ]
