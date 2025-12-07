from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
   
    queryset = Task.objects.filter(created_by=request.user).order_by('-created_at')

    #search
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    #filter by status
    status = request.GET.get('status', '').strip()
    if status in [Task.STATUS_PENDING, Task.STATUS_IN_PROGRESS, Task.STATUS_COMPLETED]:
        queryset = queryset.filter(status=status)

    # pagination 
    page_number = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10) 
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'q': q,
        'status': status,
    }
    return render(request, 'tasks/task_list.html', context)



@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'page_title': 'Create Task'
    })


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'page_title': 'Edit Task'
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {
        'task': task
    })
