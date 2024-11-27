# Generated by Django 5.1.3 on 2024-11-19 18:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unnamed Media', max_length=100)),
                ('loanDate', models.DateField(blank=True, null=True)),
                ('available', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Media',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('media_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='membre.media')),
                ('author', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Books',
            },
            bases=('membre.media',),
        ),
        migrations.CreateModel(
            name='Cd',
            fields=[
                ('media_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='membre.media')),
                ('artist', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'CDs',
            },
            bases=('membre.media',),
        ),
        migrations.CreateModel(
            name='Dvd',
            fields=[
                ('media_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='membre.media')),
                ('director', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'DVDs',
            },
            bases=('membre.media',),
        ),
    ]