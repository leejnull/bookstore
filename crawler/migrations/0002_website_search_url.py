# Generated by Django 3.0.3 on 2020-02-20 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='search_url',
            field=models.CharField(default='', max_length=256),
        ),
    ]
