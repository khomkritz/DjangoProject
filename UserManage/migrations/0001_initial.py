# Generated by Django 3.2 on 2023-11-24 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', max_length=16)),
                ('first_name', models.CharField(max_length=150, null=True)),
                ('last_name', models.CharField(max_length=150, null=True)),
                ('email', models.CharField(max_length=55, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('tel', models.CharField(max_length=9, null=True)),
                ('role', models.CharField(choices=[('PM', 'Project Manage'), ('DEV', 'Developer')], default='DEV', max_length=16)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='UserTask',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=55, null=True)),
                ('description', models.CharField(max_length=150, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN PROGRESS', 'In Progress'), ('COMPLETE', 'Complete'), ('DELETE', 'Delete')], default='PENDING', max_length=16)),
                ('user_id', models.IntegerField(default=0)),
                ('software', models.CharField(choices=[('APP', 'Application'), ('WEB', 'Website')], max_length=16)),
                ('create_by', models.IntegerField(blank=True, null=True)),
                ('update_by', models.IntegerField(blank=True, null=True)),
                ('delete_by', models.IntegerField(blank=True, null=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('delete_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_task',
            },
        ),
    ]
