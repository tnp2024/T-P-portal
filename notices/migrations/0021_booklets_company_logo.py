# Generated by Django 4.2.5 on 2024-06-13 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0020_alter_activity_company_logo_booklets'),
    ]

    operations = [
        migrations.AddField(
            model_name='booklets',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos/'),
        ),
    ]
