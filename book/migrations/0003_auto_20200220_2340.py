# Generated by Django 3.0.3 on 2020-02-20 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_novel_website_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='novel',
            unique_together={('title', 'author')},
        ),
    ]
