# Generated by Django 4.2.5 on 2024-05-21 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0037_alter_profilechange_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='Preference_1',
            field=models.CharField(blank=True, choices=[('Job', 'Job'), ('Entrepreneurship', 'Entrepreneurship'), ('Higher Studies', 'Higher Studies')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='Preference_2',
            field=models.CharField(blank=True, choices=[('Job', 'Job'), ('Entrepreneurship', 'Entrepreneurship'), ('Higher Studies', 'Higher Studies')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='Preference_3',
            field=models.CharField(blank=True, choices=[('Job', 'Job'), ('Entrepreneurship', 'Entrepreneurship'), ('Higher Studies', 'Higher Studies')], max_length=255, null=True),
        ),
    ]
