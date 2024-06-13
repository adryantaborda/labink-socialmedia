# Generated by Django 5.0.6 on 2024-06-05 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0010_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='static/images/icons/avatar.svg', null=True, upload_to='static/images/icons/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
    ]
