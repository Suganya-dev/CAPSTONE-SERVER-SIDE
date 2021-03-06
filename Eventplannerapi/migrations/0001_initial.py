# Generated by Django 3.1.7 on 2021-03-19 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventName', models.CharField(max_length=50)),
                ('eventdate', models.DateField()),
                ('venue', models.CharField(max_length=70)),
                ('numOfGuests', models.IntegerField(blank=True, null=True)),
                ('content', models.CharField(max_length=100)),
                ('approved', models.BooleanField(default=None)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eventplannerapi.category')),
            ],
        ),
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='FoodTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('foodType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eventplannerapi.foodtype')),
            ],
        ),
        migrations.CreateModel(
            name='FoodPlanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('events', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eventplannerapi.events')),
                ('foodTable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foodTable', to='Eventplannerapi.foodtable')),
            ],
        ),
        migrations.CreateModel(
            name='EventUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=100)),
                ('createdOn', models.DateField()),
                ('active', models.BooleanField(default=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='events',
            name='eventUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eventplannerapi.eventuser'),
        ),
    ]
