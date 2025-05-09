# Generated by Django 5.1.5 on 2025-05-08 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0005_rename_is_read_notification_read_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='read',
            new_name='is_read',
        ),
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
