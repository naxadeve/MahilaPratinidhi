# Generated by Django 2.0.7 on 2018-07-25 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20180724_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mahilapratinidhiform',
            name='age',
            field=models.CharField(blank=True, max_length=300, verbose_name='उमेर'),
        ),
        migrations.AlterField(
            model_name='mahilapratinidhiform',
            name='name',
            field=models.CharField(blank=True, max_length=300, verbose_name='नाम'),
        ),
    ]