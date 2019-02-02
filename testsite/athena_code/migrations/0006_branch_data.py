# Generated by Django 2.1.5 on 2019-02-09 15:05

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athena_code', '0005_auto_20190209_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Enter any additional data about the as a dict', null=True),
        ),
    ]
