# Generated by Django 3.1.3 on 2022-11-22 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testhome', '0008_auto_20221122_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elementmodule',
            name='element_id',
            field=models.IntegerField(help_text='元素id', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pagemodule',
            name='page_id',
            field=models.IntegerField(help_text='页面模块id', primary_key=True, serialize=False),
        ),
    ]
