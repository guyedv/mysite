# Generated by Django 4.0.4 on 2022-06-06 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_homework_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='chore',
            name='type',
            field=models.CharField(default='Chore', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homework',
            name='type',
            field=models.CharField(default='Homework', max_length=20),
            preserve_default=False,
        ),
    ]
