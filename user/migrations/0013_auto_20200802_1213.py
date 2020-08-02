# Generated by Django 3.0.8 on 2020-08-02 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_hotel_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='hotel_price',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='hotel_room',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='img',
        ),
        migrations.AddField(
            model_name='availability',
            name='typeofroom',
            field=models.CharField(default='deluxe', max_length=30),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='hotel_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeofroom', models.CharField(max_length=30)),
                ('hotel_room', models.IntegerField()),
                ('hotel_price', models.IntegerField(default=1000)),
                ('img', models.ImageField(upload_to='')),
                ('hotel_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.hotel')),
            ],
        ),
    ]
