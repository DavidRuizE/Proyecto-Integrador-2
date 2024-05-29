# En APP/migrations/0002_merchandise_alter_foto_phototype_foto_merchandise.py
from django.db import migrations, models

def create_default_merchandise(apps, schema_editor):
    Merchandise = apps.get_model('APP', 'Merchandise')
    Merchandise.objects.create(consecutive_number=1, weight=0.0)

class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consecutive_number', models.PositiveIntegerField(unique=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='foto',
            name='photoType',
            field=models.CharField(choices=[('Recolección', 'Recolección'), ('Descarga', 'Descarga'), ('Camion Basura', 'Camion De Basura')], default='Recolección', max_length=255),
        ),
        migrations.AddField(
            model_name='foto',
            name='merchandise',
            field=models.ForeignKey(default=1, on_delete=models.CASCADE, to='APP.Merchandise'),
            preserve_default=False,
        ),
        migrations.RunPython(create_default_merchandise),
    ]
