# Generated by Django 3.0.3 on 2020-03-09 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_crawlingrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawlingrecord',
            name='create_dt',
            field=models.DateTimeField(auto_created=True, auto_now=True),
        ),
    ]