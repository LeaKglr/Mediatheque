# Generated by Django 5.1.3 on 2024-11-26 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibliothecaire', '0008_borrow_is_blocked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrow',
            name='is_blocked',
        ),
        migrations.AddField(
            model_name='borrower',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
