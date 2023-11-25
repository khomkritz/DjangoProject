from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, UserTask
from .utils import UserDetail
from DjangoProject.settings import db_default
from datetime import datetime, timedelta


# Create your views here.
class GetUserList(APIView):
    def get(self, request):
        collect_user = []
        users = User.objects.using(db_default).all()
        for user in users:
            data_user = {
                "id" : user.id,
                "first_name" : user.first_name,
                "last_name" : user.last_name,
                "tel" : user.tel,
                "email" : user.email,
                "status" : user.status,
                "role" : user.role
            }
            collect_user.append(data_user)
        return Response({"status" : True,"message" : "get success", "data" : collect_user},status=status.HTTP_200_OK)

class CreateUser(APIView):
    def post(self, request):
        data = request.data
        check_email = User.objects.using(db_default).filter(email=data["email"]).exists()
        if check_email == True:
            return Response({"status" : False,"message" : "already have a email",}, status=status.HTTP_400_BAD_REQUEST)
        ## check email beacuse can't use email duplicate ##
        data_user = {
            "first_name" : data["first_name"],
            "last_name" : data["last_name"],
            "email" : data["email"],
            "tel" : data["tel"],
            "password" : data["password"],
            "role" : data["role"]
        }
        create_user = User.objects.using(db_default).create(**data_user)
        if create_user:
            return Response({"status" : True,"message" : "create user success"},status=status.HTTP_200_OK)
        else:
            return Response({"status" : False,"message" : "error create user",}, status=status.HTTP_400_BAD_REQUEST)

class UpdateUser(APIView):
    def put(self, request, id):
        data = request.data
        if "email" in data:
            check_email = User.objects.using(db_default).filter(email=data["email"]).exists()
            if check_email == True:
                return Response({"status" : False,"message" : "already have a email",}, status=status.HTTP_400_BAD_REQUEST)
        ## check email beacuse can't use email duplicate ##
        if "status" in data and data["status"] not in ["ACTIVE","INACTIVE"]:
            return Response({"status" : False,"message" : "error user status",}, status=status.HTTP_400_BAD_REQUEST)
        ## check status name in body will error when status name not in ["ACTIVE","INACTIVE"] ##
        update_user = User.objects.using(db_default).filter(id=id).update(**data)
        if update_user:
            user = User.objects.using(db_default).get(id=id)
            data_user = {
                "id" : user.id,
                "first_name" : user.first_name,
                "last_name" : user.last_name,
                "tel" : user.tel,
                "email" : user.email,
                "status" : user.status,
                "role" : user.role
            }
            return Response({"status" : True, "message" : "update user success", "data" : data_user},status=status.HTTP_200_OK)
        else:
            return Response({"status" : False,"message" : "error update user",}, status=status.HTTP_400_BAD_REQUEST)

class DeleteUser(APIView):
    def delete(self, request, id):
        user = User.objects.using(db_default).get(id=id)
        if user.status == "DELETE":
            return Response({"status" : False,"message" : "user was deleted",}, status=status.HTTP_400_BAD_REQUEST)
        ## check user status == DELETE will response error ##
        user.status = "DELETE"
        user.delete_at = datetime.now()
        user.save()
        return Response({"status" : True,"message" : "delete user success"},status=status.HTTP_200_OK)
    
class GetTaskList(APIView):
    def get(self, request):
        collect_task = []
        status_name = request.GET.get("status")
        software = request.GET.get("software")
        date_start = request.GET.get("date_start")
        date_end = request.GET.get("date_end")
        tasks = UserTask.objects.using(db_default).all()
        if status_name != None:
            tasks = tasks.filter(status=status_name)
        elif software != None:
            tasks = tasks.filter(software=software)
        elif date_start != None and date_end != None:
            tasks = tasks.filter(due_date__range=(datetime.strptime(date_start, '%Y-%m-%d'), (datetime.strptime(date_end, '%Y-%m-%d') + timedelta(minutes=1439))))
        ## this code will filter when have params status, software, date_start and date_end will filter data ##
        for task in tasks:
            user_detail = None
            if (task.user_id != None) and (task.user_id != 0):
                user = User.objects.using(db_default).get(id=task.user_id)
                user_detail = {
                    "id" : user.id,
                    "name" : str(user.first_name)+' '+str(user.last_name),
                    "role" : user.role
                }
            data_task = {
                "id" : task.id,
                "title" : task.title,
                "description" : task.description,
                "software" : task.software,
                "status" : task.status,
                "user" : user_detail,
                "due_date" : task.due_date
            }
            collect_task.append(data_task)
        return Response({"status" : True,"message" : "get success", "data" : collect_task},status=status.HTTP_200_OK)
    
class GetTaskDetail(APIView):
    def get(self, request, id):
        task = UserTask.objects.using(db_default).get(id=id)
        user_detail = None
        create_by = None
        update_by = None
        delete_by = None
        if (task.user_id != None) and (task.user_id != 0):
            user_detail = UserDetail(task.user_id)
        if (task.create_by != None) and (task.create_by != 0):
            create_by = UserDetail(task.create_by)
        if (task.update_by != None) and (task.update_by != 0):
            update_by = UserDetail(task.update_by)
        if (task.delete_by != None) and (task.delete_by != 0):
            delete_by = UserDetail(task.delete_by)
        ## i use function UserDetail because clean code ##
        data_task = {
            "id" : task.id,
            "title" : task.title,
            "description" : task.description,
            "software" : task.software,
            "status" : task.status,
            "user" : user_detail,
            "due_date" : task.due_date,
            "create_by" : create_by,
            "update_by" : update_by,
            "delete_by" : delete_by,
            "create_at" : task.create_at,
            "update_at" : task.update_at,
            "delete_at" : task.delete_at
        }
        return Response({"status" : True,"message" : "get success", "data" : data_task},status=status.HTTP_200_OK)
    
class CreateTask(APIView):
    def post(self, request):
        data = request.data
        create_by = request.GET.get("create_by")
        if create_by == None:
            return Response({"status" : False,"message" : "require user id for create",}, status=status.HTTP_400_BAD_REQUEST)
        ## require user id to create make me know who are create this task ##
        task_status = "PENDING"
        if "user_id" in data and data["user_id"] != None:
            task_status = "IN PROGRESS"
        ## this code is check when create task if have user_id or user_id != None , this task will status = IN PROGRESS because add task to user ##
        data_taks = {
            "title" : data["title"],
            "description" : data["description"],
            "status" : task_status,
            "user_id" : data["user_id"],
            "software" :data["software"],
            "due_date" : datetime.strptime(data["due_date"], '%Y-%m-%d') + timedelta(minutes=1439),
            "create_by" : create_by
        }
        create_task = UserTask.objects.using(db_default).create(**data_taks)
        if create_task:
            return Response({"status" : True,"message" : "create task success"},status=status.HTTP_200_OK)
        else:
            return Response({"status" : False,"message" : "error create task",}, status=status.HTTP_400_BAD_REQUEST)

class UpdateTask(APIView):
    def put(self, request, id):
        data = request.data
        update_by = request.GET.get("update_by")
        if update_by == None:
            return Response({"status" : False,"message" : "require user id for update",}, status=status.HTTP_400_BAD_REQUEST)
        ## require user id to update make me know who are update this task ##
        if "due_date" in data and data["due_date"] != None:
            data["due_date"] = datetime.strptime(data["due_date"], '%Y-%m-%d') + timedelta(minutes=1439)
        ## this code when have data name due_date in body will + time 24:59 to due_date
        if "status" in data and data["status"] not in ["PENDING","IN PROGRESS","COMPLETE"]:
            return Response({"status" : False,"message" : "error user status",}, status=status.HTTP_400_BAD_REQUEST)
        ## check status name in body will error when status name not in ["PENDING","IN PROGRESS","COMPLETE"] ##
        data["update_by"] = update_by
        data["update_at"] = datetime.now()
        update_task = UserTask.objects.using(db_default).filter(id=id).update(**data)
        if update_task:
            task = UserTask.objects.using(db_default).get(id=id)
            user_detail = None
            if (task.user_id != None) and (task.user_id != 0):
                user = User.objects.using(db_default).get(id=task.user_id)
                user_detail = {
                    "id" : user.id,
                    "name" : str(user.first_name)+' '+str(user.last_name),
                    "role" : user.role
                }
            data_task = {
                "id" : task.id,
                "title" : task.title,
                "description" : task.description,
                "software" : task.software,
                "status" : task.status,
                "user" : user_detail,
                "due_date" : task.due_date
            }
            return Response({"status" : True, "message" : "update task success", "data" : data_task},status=status.HTTP_200_OK)
        else:
            return Response({"status" : False,"message" : "error update task",}, status=status.HTTP_400_BAD_REQUEST)

        
class DeleteTask(APIView):
    def delete(self, request, id):
        delete_by = request.GET.get("delete_by")
        if delete_by == None:
            return Response({"status" : False,"message" : "require user id for delete",}, status=status.HTTP_400_BAD_REQUEST)
        ## require user id to delete make me know who are delete this task ##
        task = UserTask.objects.using(db_default).get(id=id)
        if task.status == "DELETE":
            return Response({"status" : False,"message" : "task was deleted",}, status=status.HTTP_400_BAD_REQUEST)
        task.status = "DELETE"
        task.delete_at = datetime.now()
        task.delete_by = delete_by
        task.save()
        return Response({"status" : True,"message" : "delete task success"},status=status.HTTP_200_OK)