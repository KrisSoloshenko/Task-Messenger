# Generated by Django 5.1.5 on 2025-01-31 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_room_photo_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='photo',
            field=models.ImageField(blank=True, default='room/room.png', null=True, upload_to='room/', verbose_name='фотография'),
        ),
    ]
