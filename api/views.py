from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view

from mainApp.models import Task
from .serializers import *


@api_view(['GET'])
def api_root(request, format=None):
    return redirect(reverse('mainApp:list_create'))


class TaskListCreateView(LoginRequiredMixin, ListCreateAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailUpdateDeleteView(LoginRequiredMixin, RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TaskUpdateSerializer
        return TaskListSerializer

    def perform_update(self, serializer):
        task = self.get_object()
        if task.owner == self.request.user:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("Not Allowed")

    def perform_destroy(self, instance):
        if instance.owner == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("Not Allowed")
