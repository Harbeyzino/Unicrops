# Generated by Django 5.1.6 on 2025-02-24 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('client_name', models.CharField(max_length=200)),
                ('service', models.CharField(max_length=200)),
            ],
        ),
    ]
