# Generated by Django 4.2.3 on 2024-06-04 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_userchoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testmodel',
            name='name',
            field=models.TextField(max_length=500),
        ),
    ]