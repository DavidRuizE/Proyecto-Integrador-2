# Generated by Django 5.0.1 on 2024-05-29 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0004_foto_weight_alter_foto_phototype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='foto',
            name='material_type',
            field=models.CharField(choices=[('Botellas de Amor', 'Botellas de Amor'), ('Otros Materiales', 'Otros Materiales')], default='Botellas de Amor', max_length=255),
        ),
    ]
