# Generated by Django 2.1.7 on 2019-02-20 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athena_code', '0017_auto_20190216_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='include',
            field=models.CharField(blank=True, default='', help_text='use -Ipath when compiling', max_length=500),
        ),
        migrations.AddField(
            model_name='configuration',
            name='lib',
            field=models.CharField(blank=True, default='', help_text='use -Lpath when linking', max_length=500),
        ),
    ]
