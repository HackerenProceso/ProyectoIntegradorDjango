# Generated by Django 5.0.6 on 2024-06-27 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0028_alter_marca_imagen_alter_productoimagen_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='imagen',
            field=models.ImageField(upload_to='categorias'),
        ),
    ]
