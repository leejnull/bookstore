# Generated by Django 3.0.3 on 2020-03-09 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20200301_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='create_time',
            field=models.DateTimeField(auto_created=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]