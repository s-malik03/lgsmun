# Generated by Django 3.1.5 on 2021-01-11 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0004_auto_20210111_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committee', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('duration', models.IntegerField()),
            ],
        ),
    ]
