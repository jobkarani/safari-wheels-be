# Generated by Django 5.0.7 on 2024-08-02 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_profile_phonenumber_profile_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['rating']},
        ),
        migrations.RemoveField(
            model_name='review',
            name='created_at',
        ),
    ]
