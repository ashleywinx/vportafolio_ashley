# Generated by Django 3.2 on 2024-12-09 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appportafolio', '0017_trabajo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('asignatura', models.CharField(blank=True, max_length=200, null=True, verbose_name='Asignatura')),
                ('nota', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='Nota')),
            ],
            options={
                'verbose_name': 'Calificacion',
                'verbose_name_plural': 'Calificaciones',
                'ordering': ['id'],
            },
        ),
    ]
