# Generated by Django 5.0.6 on 2024-06-12 05:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0022_remove_cliente_is_active_remove_cliente_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='fecha_de_registro',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
