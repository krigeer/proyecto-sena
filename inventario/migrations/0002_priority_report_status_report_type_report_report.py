# Generated by Django 5.1.1 on 2025-04-17 06:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority_report',
            fields=[
                ('id_priority_report', models.AutoField(primary_key=True, serialize=False)),
                ('name_priority_report', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status_report',
            fields=[
                ('id_status_report', models.AutoField(primary_key=True, serialize=False)),
                ('name_status_report', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type_report',
            fields=[
                ('id_type_report', models.AutoField(primary_key=True, serialize=False)),
                ('name_type_report', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id_report', models.AutoField(primary_key=True, serialize=False)),
                ('observation', models.TextField()),
                ('date_report', models.DateTimeField(auto_now=True)),
                ('idMaterial_didactico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.material_didactico')),
                ('idTecnology', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.tecnology')),
                ('id_centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.centro')),
                ('id_priority_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.priority_report')),
                ('id_ubication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.ubication')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.user')),
                ('id_status_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.status_report')),
                ('id_type_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.type_report')),
            ],
        ),
    ]
