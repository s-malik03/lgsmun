# Generated by Django 3.1.5 on 2021-01-19 05:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dashboards', '0009_auto_20210118_1931'),
    ]

    operations = [
        migrations.CreateModel(
            name='FloorMods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mod', models.TextField()),
                ('committee', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
