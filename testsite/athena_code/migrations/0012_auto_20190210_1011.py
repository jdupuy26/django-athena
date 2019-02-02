# Generated by Django 2.1.5 on 2019-02-10 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athena_code', '0011_auto_20190210_0924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='fork',
        ),
        migrations.AddField(
            model_name='code',
            name='forks',
            field=models.ManyToManyField(help_text='Select a fork for this code.', to='athena_code.Fork'),
        ),
        migrations.AddField(
            model_name='fork',
            name='codes',
            field=models.ManyToManyField(help_text='Select a code for this fork', to='athena_code.Code'),
        ),
    ]