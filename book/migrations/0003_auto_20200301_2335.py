# Generated by Django 3.0.3 on 2020-03-01 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20200228_2354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='novel_id',
            new_name='book_id',
        ),
        migrations.AlterField(
            model_name='chapter',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
