# Generated by Django 5.0.1 on 2024-05-29 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0003_foto_punto_acopio'),
    ]

    operations = [
        migrations.AddField(
            model_name='foto',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='foto',
            name='photoType',
            field=models.CharField(choices=[('Remisión', 'Remisión'), ('Pesajes', 'Pesajes'), ('Descargue', 'Descargue'), ('Puntos de acopio', 'Puntos de acopio')], default='Remisión', max_length=255),
        ),
        migrations.AlterField(
            model_name='foto',
            name='punto_acopio',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]