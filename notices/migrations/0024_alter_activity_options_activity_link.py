# Generated by Django 4.2.5 on 2024-07-01 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0023_alter_activity_activity_status_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ['-creation_date']},
        ),
        migrations.AddField(
            model_name='activity',
            name='link',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]