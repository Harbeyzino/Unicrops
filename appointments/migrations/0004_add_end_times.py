from django.db import migrations, models
from datetime import datetime, timedelta

def populate_end_times(apps, schema_editor):
    TimeSlot = apps.get_model('appointments', 'TimeSlot')
    for slot in TimeSlot.objects.all():
        # Set end_time to 30 minutes after start time
        slot_end = (datetime.combine(datetime.today(), slot.time) + 
                   timedelta(minutes=30)).time()
        slot.end_time = slot_end
        slot.save()

class Migration(migrations.Migration):
    dependencies = [
        # Replace '0003_previous' with your actual last migration filename
        ('appointments', '0003_auto_20250501_1604'),  
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.RunPython(populate_end_times),
        migrations.AlterField(
            model_name='timeslot',
            name='end_time',
            field=models.TimeField(),  # Now make non-nullable
        ),
    ]