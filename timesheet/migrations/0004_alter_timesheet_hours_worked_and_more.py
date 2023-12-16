# Generated by Django 4.2.7 on 2023-12-16 12:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("timesheet", "0003_timesheet"),
    ]

    operations = [
        migrations.AlterField(
            model_name="timesheet",
            name="hours_worked",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name="timesheet",
            name="week_start_date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]