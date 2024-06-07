# Generated by Django 5.0.6 on 2024-06-07 19:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_groups_group_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='game',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.games'),
        ),
    ]