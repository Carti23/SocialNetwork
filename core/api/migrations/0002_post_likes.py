# Generated by Django 3.1.2 on 2022-04-03 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
