# Generated by Django 5.1.3 on 2024-11-24 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0003_alter_book_options_alter_cd_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cd',
            name='media_ptr',
        ),
        migrations.RemoveField(
            model_name='dvd',
            name='media_ptr',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Cd',
        ),
        migrations.DeleteModel(
            name='Dvd',
        ),
        migrations.DeleteModel(
            name='Media',
        ),
    ]
