# Generated by Django 5.1.5 on 2025-05-08 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0004_notification_project_task_subtask_taskprogress_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='is_read',
            new_name='read',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='link',
        ),
    ]
