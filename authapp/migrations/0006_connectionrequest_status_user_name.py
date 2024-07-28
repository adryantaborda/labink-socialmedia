# Generated by Django 5.0.6 on 2024-07-26 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_remove_connectionrequest_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectionrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
