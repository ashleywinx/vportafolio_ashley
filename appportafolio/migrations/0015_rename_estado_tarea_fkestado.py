# Generated by Django 3.2 on 2024-12-05 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appportafolio', '0014_auto_20241204_1355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarea',
            old_name='estado',
            new_name='fkestado',
        ),
    ]
