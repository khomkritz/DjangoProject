from django.urls import path, include
from UserManage import views

urlpatterns = [
    path('get_list',views.GetUserList.as_view()),
    path('create', views.CreateUser.as_view()),
    path('update/<int:id>', views.UpdateUser.as_view()),
    path('delete/<int:id>',views.DeleteUser.as_view()),
    path('task/get_list', views.GetTaskList.as_view()),
    path('task/get_detail/<int:id>', views.GetTaskDetail.as_view()),
    path('task/create', views.CreateTask.as_view()),
    path('task/update/<int:id>', views.UpdateTask.as_view()),
    path('task/delete/<int:id>', views.DeleteTask.as_view()),
]