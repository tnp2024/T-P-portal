# Generated by Django 4.2.5 on 2024-06-03 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0040_alter_otp_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OTP',
        ),
    ]