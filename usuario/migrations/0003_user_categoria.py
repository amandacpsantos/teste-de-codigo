# Generated by Django 2.1.7 on 2019-02-14 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_auto_20190214_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='categoria',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
