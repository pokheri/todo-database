from django.urls import path
from . import views


urlpatterns = [
    path("create-task/", views.CreateNewTaskAPIView.as_view(), name="create-task"),
    path("tasks/", views.ListTasksAPIView.as_view(), name="tasks"),
    path(
        "update-task/<str:pk>/", views.UpdateTaskApiView.as_view(), name="update_task"
    ),
    path(
        "delete-task/<str:pk>/", views.DeleteTaskApiView.as_view(), name="delete_task"
    ),
]
