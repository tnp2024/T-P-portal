# Generated by Django 4.2.5 on 2024-03-19 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0007_alter_activity_reference_no'),
        ('users', '0016_rename_student_activityapplication_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activityapplication',
            old_name='FIRST_NAME',
            new_name='PRN',
        ),
        migrations.RenameField(
            model_name='activityapplication',
            old_name='title',
            new_name='activity_id',
        ),
        migrations.RenameField(
            model_name='driveapplication',
            old_name='FIRST_NAME',
            new_name='PRN',
        ),
        migrations.RenameField(
            model_name='driveapplication',
            old_name='title',
            new_name='drive_id',
        ),
        migrations.AlterUniqueTogether(
            name='activityapplication',
            unique_together={('activity_id', 'PRN')},
        ),
        migrations.AlterUniqueTogether(
            name='driveapplication',
            unique_together={('drive_id', 'PRN')},
        ),
    ]
