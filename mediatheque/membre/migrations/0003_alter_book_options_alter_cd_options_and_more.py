# Generated by Django 5.1.3 on 2024-11-19 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0002_alter_book_options_alter_cd_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name_plural': 'Books'},
        ),
        migrations.AlterModelOptions(
            name='cd',
            options={'verbose_name_plural': 'CDs'},
        ),
        migrations.AlterModelOptions(
            name='dvd',
            options={'verbose_name_plural': 'DVDs'},
        ),
        migrations.AlterModelOptions(
            name='media',
            options={'verbose_name_plural': 'Media'},
        ),
    ]
