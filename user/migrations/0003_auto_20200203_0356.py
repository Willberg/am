# Generated by Django 3.0.2 on 2020-02-03 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200201_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='create_time',
            field=models.BigIntegerField(default=1580702218636),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='update_time',
            field=models.BigIntegerField(default=1580702218636),
        ),
    ]