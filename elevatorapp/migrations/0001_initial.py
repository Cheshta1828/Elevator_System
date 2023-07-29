# Generated by Django 4.2.3 on 2023-07-29 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b_name', models.CharField(max_length=50)),
                ('total_elevators', models.PositiveSmallIntegerField()),
                ('minimumfloors', models.IntegerField(default=0)),
                ('totalfloors', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ElevatorRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_floor', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_number', models.IntegerField()),
                ('status', models.CharField(choices=[('UP', 'UP'), ('IDLE', 'IDLE'), ('DOWN', 'DOWN')], default='IDLE', max_length=4)),
                ('current_floor', models.IntegerField(default=0)),
                ('is_running', models.BooleanField(default=False)),
                ('is_door_open', models.BooleanField(default=False)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elevatorapp.building')),
            ],
        ),
    ]
