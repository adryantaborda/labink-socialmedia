# Generated by Django 5.0.6 on 2024-06-04 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0009_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='static/images/icons/avatar.svg', null=True, upload_to='static/images/icons/'),
        ),
    ]