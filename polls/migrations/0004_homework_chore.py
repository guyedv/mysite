# Generated by Django 4.0.4 on 2022-06-02 08:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_delete_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('active', 'Active'), ('done', 'Done')], max_length=255)),
                ('course', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=200)),
                ('ownerId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homeworks', to='polls.person')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Chore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('active', 'Active'), ('done', 'Done')], max_length=255)),
                ('description', models.CharField(max_length=200)),
                ('size', models.CharField(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], max_length=255)),
                ('ownerId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chores', to='polls.person')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
