# Generated by Django 4.1.5 on 2023-03-19 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_alter_project_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='features',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]