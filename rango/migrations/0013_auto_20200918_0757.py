# Generated by Django 2.1.5 on 2020-09-18 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0012_auto_20200918_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='emailAddress',
            field=models.EmailField(default='empty@emailaddress.com', max_length=254),
        ),
    ]
