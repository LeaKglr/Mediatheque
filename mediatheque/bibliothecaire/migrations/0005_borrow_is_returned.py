# Generated by Django 5.1.3 on 2024-11-18 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibliothecaire', '0004_borrow'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
    ]