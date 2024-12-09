# Generated by Django 3.2 on 2024-12-09 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appportafolio', '0016_auto_20241206_1920'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trabajo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(blank=True, max_length=200, null=True, verbose_name='nombre proyecto')),
                ('lenguaje', models.CharField(max_length=100, verbose_name='Estado')),
                ('tecnologias', models.CharField(max_length=100, verbose_name='Estado')),
                ('observaciones', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('fecha_proyecto', models.DateField(auto_now_add=True, verbose_name='Fecha de envio')),
            ],
            options={
                'verbose_name': 'Trabajo',
                'verbose_name_plural': 'Trabajos',
                'ordering': ['fecha_proyecto'],
            },
        ),
    ]