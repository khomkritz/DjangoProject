# Generated by Django 3.2 on 2023-11-24 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManage', '0002_auto_20231124_0516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertask',
            name='user_id',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
