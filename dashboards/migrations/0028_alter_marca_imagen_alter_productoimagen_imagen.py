# Generated by Django 5.0.6 on 2024-06-27 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0027_remove_detalleorden_subtotal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marca',
            name='imagen',
            field=models.ImageField(upload_to='marcas'),
        ),
        migrations.AlterField(
            model_name='productoimagen',
            name='imagen',
            field=models.ImageField(upload_to='productos'),
        ),
    ]
