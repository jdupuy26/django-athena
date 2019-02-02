# Generated by Django 2.1.5 on 2019-02-16 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athena_code', '0015_auto_20190216_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='fork',
        ),
        migrations.AlterField(
            model_name='configuration',
            name='ccmd',
            field=models.CharField(blank=True, default='', help_text='Override for command to used to call C++ compiler', max_length=100),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='cflag',
            field=models.CharField(blank=True, default='', help_text='Addition str of flags to append to compiler/linker call', max_length=100),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='fftw_path',
            field=models.CharField(blank=True, default='', help_text='Enter path to FFTW libraries', max_length=100),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='hdf5_path',
            field=models.CharField(blank=True, default='', help_text='Enter path to HDF5 libraries', max_length=100),
        ),
    ]