# Generated by Django 5.0.6 on 2024-06-14 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0025_alter_cliente_email_alter_cliente_groups_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrito',
            name='total',
        ),
        migrations.RemoveField(
            model_name='detallecarrito',
            name='subtotal',
        ),
    ]
