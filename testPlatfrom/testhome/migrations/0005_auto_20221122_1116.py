# Generated by Django 3.1.3 on 2022-11-22 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testhome', '0004_auto_20221122_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagemodule',
            name='id',
            field=models.CharField(default=1, help_text='页面模块id', max_length=8, primary_key=True, serialize=False),
        ),
    ]
