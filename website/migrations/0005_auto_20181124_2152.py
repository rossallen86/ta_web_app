# Generated by Django 2.1.2 on 2018-11-24 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20181124_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email_address',
            field=models.EmailField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='street_address',
            field=models.CharField(max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='lab',
            field=models.CharField(max_length=3, null=True),
        ),
    ]