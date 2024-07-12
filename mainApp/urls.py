from django.urls import path
from . import views

app_name = 'mainApp'

urlpatterns = [
    path('', views.TaskListCreateView.as_view(), name='list_create'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
]
