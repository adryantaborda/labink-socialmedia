# Generated by Django 5.0.6 on 2024-06-12 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0019_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='avatardefault.png', null=True, upload_to='media/'),
        ),
    ]
