# Generated by Django 4.2.5 on 2024-03-11 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('S', 'Student'), ('C', 'Coordinator'), ('T-O', 'TNP-Office')], default='Student', max_length=10),
        ),
    ]
