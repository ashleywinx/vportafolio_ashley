# Generated by Django 3.2 on 2024-12-04 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appportafolio', '0013_estado_tarea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='fecha',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Fecha y Hora'),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='tarea',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Anotar Tarea'),
        ),
    ]
