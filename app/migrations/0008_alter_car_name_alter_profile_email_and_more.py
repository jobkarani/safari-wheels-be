# Generated by Django 5.0.7 on 2024-08-22 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_car_owner_profile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
