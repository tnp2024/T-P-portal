# Generated by Django 4.2.5 on 2024-03-18 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='Pass_out_Year',
            field=models.CharField(choices=[('2024', '2024')], default='2024', max_length=10),
        ),
        migrations.AlterField(
            model_name='student',
            name='Profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/profiles/'),
        ),
    ]
