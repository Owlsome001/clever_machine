# Generated by Django 4.1.5 on 2023-03-18 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
