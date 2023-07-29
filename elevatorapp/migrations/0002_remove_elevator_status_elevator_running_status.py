# Generated by Django 4.2.3 on 2023-07-29 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevatorapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elevator',
            name='status',
        ),
        migrations.AddField(
            model_name='elevator',
            name='running_status',
            field=models.CharField(choices=[('going_up', 'Going_Up'), ('standing_still', 'Standing_Still'), ('going_down', 'Going_Down'), ('not_working', 'Not_Working')], default='standing_still', max_length=20),
        ),
    ]