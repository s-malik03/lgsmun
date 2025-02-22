# Generated by Django 3.1.5 on 2021-01-09 07:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('dashboards', '0002_auto_20210108_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitteeControl',
            fields=[
                ('committee', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('speaking_mode', models.CharField(default='Idle', max_length=100)),
                ('allow_motions', models.BooleanField()),
                ('topic', models.CharField(default='No Topic Has Been Set', max_length=100)),
                ('current_mod', models.CharField(default='No Moderated Caucus in Progress', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committee', models.CharField(max_length=100)),
                ('sender', models.CharField(max_length=100)),
                ('recipient', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=250)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committee', models.CharField(max_length=100)),
                ('topic', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('committee', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committee', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('vote_status', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='placard',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='gsl',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rsl',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
