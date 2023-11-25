from django.db import models

# Create your models here.
class User(models.Model):
    role_list = (
        ('PM', 'Project Manage'),
        ('DEV', 'Developer'),
    )
    status_list = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('DELETE', 'Delete'),
    )
    class Meta:
        db_table = "user"
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=16, choices=status_list, default='ACTIVE')
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=55, unique=True)
    password = models.CharField(max_length=200)
    tel = models.CharField(max_length=9, null=True)
    role = models.CharField(max_length=16, choices=role_list, default='DEV')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True)

class UserTask(models.Model):
    software_list = (
        ('APP', 'Application'),
        ('WEB', 'Website')
    )
    status_list = (
        ('PENDING', 'Pending'),
        ('IN PROGRESS', 'In Progress'),
        ('COMPLETE', 'Complete'),
        ('DELETE', 'Delete'),
    )
    class Meta:
        db_table = "user_task"
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=55, null=True)
    description = models.CharField(max_length=150, null=True)
    status = models.CharField(max_length=16, choices=status_list, default='PENDING')
    user_id = models.IntegerField(default=None, null=True)
    software = models.CharField(max_length=16, choices=software_list)
    create_by = models.IntegerField(null=True, blank=True)
    update_by = models.IntegerField(null=True, blank=True)
    delete_by = models.IntegerField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True)
    