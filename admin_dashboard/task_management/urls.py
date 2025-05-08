from django.urls import path
from . import views

urlpatterns = [
    path('projects/<int:project_id>/tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/subtasks/add/', views.add_subtask, name='add_subtask'),
    path('tasks/<int:task_id>/progress/', views.update_progress, name='update_progress'),
    path('progress/<int:progress_id>/comment/', views.add_comment, name='add_comment'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
]