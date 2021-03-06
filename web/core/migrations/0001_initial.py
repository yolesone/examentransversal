# Generated by Django 3.1.1 on 2022-07-11 19:56

import core.models
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
            name='Estado',
            fields=[
                ('id_estado', models.AutoField(db_column='idEstado', primary_key=True, serialize=False)),
                ('estado', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('idProducto', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('nombreProducto', models.CharField(blank=True, max_length=30, null=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('precio', models.IntegerField(blank=True, null=True)),
                ('activo', models.IntegerField(blank=True, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to=core.models.cargarFoto)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('estado', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='core.estado')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'venta',
                'verbose_name_plural': 'ventas',
                'db_table': 'ventas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('producto_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('venta_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.venta')),
            ],
            options={
                'verbose_name': 'Detalle Venta',
                'verbose_name_plural': 'Detalle Ventas',
                'db_table': 'detalleventas',
                'ordering': ['id'],
            },
        ),
    ]
