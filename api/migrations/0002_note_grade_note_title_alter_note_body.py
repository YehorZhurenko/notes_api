# Generated by Django 4.1.6 on 2023-02-10 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='grade',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='note',
            name='title',
            field=models.TextField(default='empty'),
        ),
        migrations.AlterField(
            model_name='note',
            name='body',
            field=models.TextField(default='empty'),
        ),
    ]
