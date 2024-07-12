from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from .models import Task
from .forms import TaskForm

# Django Views


@login_required
def task_list(request):
    search_query = request.GET.get('search', '')
    tasks = Task.objects.all().order_by('-created_at')
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query))
    return render(request, 'mainApp/task_list.html', {'tasks': tasks, 'search_query': search_query})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'mainApp/task_detail.html', {'task': task})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('list_create')
    else:
        form = TaskForm()
    return render(request, 'mainApp/task_form.html', {'form': form, 'form_title': 'Add Task', 'button_text': 'Create'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit this task")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('list_create')
    else:
        form = TaskForm(instance=task)
    return render(request, 'mainApp/task_form.html', {'form': form, 'form_title': 'Edit Task', 'button_text': 'Update'})


@login_required
@csrf_exempt
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this task")

    if request.method == 'POST':
        task.delete()
        return redirect('list_create')
    return render(request, 'mainApp/task_confirm_delete.html', {'task': task})


class TaskBaseView(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]


class TaskListCreateView(TaskBaseView):
    template_name = 'mainApp/task_list.html'

    def get(self, request):
        tasks = Task.objects.all().order_by('-created_at')
        search_query = request.GET.get('search', '')
        if search_query:
            tasks = tasks.filter(Q(title__icontains=search_query))
        else:
            tasks = Task.objects.all()
        return render(request, 'mainApp/task_list.html', {'tasks': tasks, 'search_query': search_query})


class TaskCreateView(TaskBaseView):
    template_name = 'mainApp/task_form.html'
    
    def get(self, request):
        form = TaskForm()
        return render(request, 'mainApp/task_form.html', {'form': form, 'form_title': 'Add Task', 'button_text': 'Create'})
    
    
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect(reverse_lazy('mainApp:list_create'))
        else:
            form = TaskForm()
        return render(request, 'mainApp/task_form.html', {'form': form, 'form_title': 'Add Task', 'button_text': 'Create'})


class TaskDetailView(TaskBaseView):
    template_name = 'mainApp/task_detail.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'mainApp/task_detail.html', {'task': task})


class TaskDeleteView(TaskBaseView):
    template_name = 'mainApp/task_confirm_delete.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.owner != request.user:
            return HttpResponseForbidden("You are not allowed to delete this task")
        return render(request, 'mainApp/task_confirm_delete.html', {'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.owner == request.user:
            task.delete()
        else:
            return HttpResponseForbidden("You are not allowed to delete this task")
        return redirect(reverse_lazy('mainApp:list_create'))


class TaskUpdateView(TaskBaseView):
    template_name = 'mainApp/task_form.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.owner != request.user:
            return HttpResponseForbidden("You are not allowed to edit this task")

        form = TaskForm(instance=task)
        return render(request, 'mainApp/task_form.html', {'form': form, 'form_title': 'Edit Task', 'button_text': 'Update'})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.owner != request.user:
            return HttpResponseForbidden("You are not allowed to edit this task")

        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('mainApp:list_create'))
        return render(request, 'mainApp/task_form.html', {'form': form})
