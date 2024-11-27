# Generated by Django 5.1.3 on 2024-11-17 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibliothecaire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='creator_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='media',
            name='creator_type',
            field=models.CharField(choices=[('author', 'author'), ('director', 'director'), ('artist', 'artist')], default='author', max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='cd',
            name='artist',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dvd',
            name='director',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='media',
            name='loanDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='media_type',
            field=models.CharField(choices=[('book', 'Book'), ('dvd', 'DVD'), ('cd', 'CD')], default='book', max_length=50),
        ),
    ]