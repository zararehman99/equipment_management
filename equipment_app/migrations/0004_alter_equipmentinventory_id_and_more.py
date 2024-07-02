# Generated by Django 4.2.3 on 2024-06-24 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment_app', '0003_accounts_addresses_equipmentcategory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentinventory',
            name='ID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='equipment_app.equipmentdetails'),
        ),
        migrations.AlterField(
            model_name='reservationstatus',
            name='RESERVATION_ID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='equipment_app.reservations'),
        ),
        migrations.AlterField(
            model_name='usersignupstatus',
            name='USER_ID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='equipment_app.accounts'),
        ),
    ]
