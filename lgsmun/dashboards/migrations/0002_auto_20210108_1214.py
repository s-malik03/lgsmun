# Generated by Django 3.1.5 on 2021-01-08 07:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dashboards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(default='Absent', max_length=50),
        ),
    ]
