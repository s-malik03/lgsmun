# Generated by Django 3.1.5 on 2021-01-06 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('committee', models.CharField(max_length=100)),
                ('school', models.CharField(max_length=100)),
            ],
        ),
    ]
