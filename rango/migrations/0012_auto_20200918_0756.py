# Generated by Django 2.1.5 on 2020-09-18 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0011_auto_20200906_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherprofile',
            name='emailAddress',
            field=models.EmailField(default='empty@emailaddress.com', max_length=254),
        ),
    ]
