# Generated by Django 5.0.1 on 2024-02-10 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Truck', '0003_alter_truckmodel_name'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='truckmodel',
            name='Truck_truck_rel_dis_365beb_idx',
        ),
    ]