from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from django.db.models import Q



@login_required
def task_list(request):
    
    queryset = Task.objects.filter(
        Q(created_by=request.user) | Q(assigned_to=request.user)
    ).order_by('-created_at').distinct()

    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    status = request.GET.get('status', '').strip()
    if status in [Task.STATUS_PENDING, Task.STATUS_IN_PROGRESS, Task.STATUS_COMPLETED]:
        queryset = queryset.filter(status=status)

    from django.core.paginator import Paginator
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
    task = get_object_or_404(
        Task.objects.filter(
            Q(created_by=request.user) | Q(assigned_to=request.user)
        ),
        pk=pk
    )

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
@login_required
@require_POST
@login_required
@require_POST
def task_toggle_status(request, pk):
    """
    Toggle a task's status between pending and completed via Ajax.
    Allowed for the creator or the assigned user.
    """

    try:
        task = Task.objects.get(
            Q(pk=pk) &
            (Q(created_by=request.user) | Q(assigned_to=request.user))
        )
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)

    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

    if task.status == Task.STATUS_COMPLETED:
        task.status = Task.STATUS_PENDING
    else:
        task.status = Task.STATUS_COMPLETED

    task.save()

    return JsonResponse({
        'success': True,
        'status': task.status,
        'status_display': task.get_status_display(),
    })
