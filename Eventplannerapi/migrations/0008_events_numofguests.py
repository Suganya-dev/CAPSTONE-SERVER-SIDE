# Generated by Django 3.1.7 on 2021-03-07 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventplannerapi', '0007_auto_20210307_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='numOfGuests',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
