# Generated by Django 3.0.4 on 2020-07-30 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200729_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='password',
            field=models.CharField(default=123456789, max_length=100),
            preserve_default=False,
        ),
    ]