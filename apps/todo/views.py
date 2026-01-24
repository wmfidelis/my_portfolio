from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Case, When, IntegerField
from django.utils import timezone
from .models import Task
from .forms import TaskForm, TaskFilterForm

@login_required
def task_list(request):
    """Display list of user's tasks with filtering and sorting"""
    tasks = Task.objects.filter(user=request.user)
    
    # Apply filters
    filter_form = TaskFilterForm(request.GET)
    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        status = filter_form.cleaned_data.get('status')
        priority = filter_form.cleaned_data.get('priority')
        sort_by = filter_form.cleaned_data.get('sort_by')
        
        if search:
            tasks = tasks.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        
        if status:
            tasks = tasks.filter(status=status)
        
        if priority:
            tasks = tasks.filter(priority=priority)
        
        # Sorting
        if sort_by == 'due_date':
            # Sort by due date, with tasks without due dates last
            tasks = tasks.order_by(
                Case(
                    When(due_date__isnull=True, then=1),
                    default=0,
                    output_field=IntegerField(),
                ),
                'due_date'
            )
        elif sort_by == 'priority':
            # Custom priority order: urgent, high, medium, low
            tasks = tasks.order_by(
                Case(
                    When(priority='urgent', then=0),
                    When(priority='high', then=1),
                    When(priority='medium', then=2),
                    When(priority='low', then=3),
                    output_field=IntegerField(),
                )
            )
        elif sort_by == 'title':
            tasks = tasks.order_by('title')
    # AFTER filters + sorting logic
    tasks = tasks.order_by('priority', 'status')
    
    # Get statistics
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, status='completed').count()
    pending_tasks = Task.objects.filter(user=request.user).exclude(status='completed').count()
    overdue_tasks = sum(1 for task in tasks if task.is_overdue)
    tasks = tasks.order_by('priority', 'status')

    
    context = {
        'tasks': tasks,
        'filter_form': filter_form,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
    }
    return render(request, 'todo/task_list.html', context)


@login_required
def task_detail(request, pk):
    """Display single task details"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    context = {
        'task': task,
    }
    return render(request, 'todo/task_detail.html', context)


@login_required
def task_create(request):
    """Create new task"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect('todo:task_list')
    else:
        form = TaskForm()
    
    context = {
        'form': form,
        'title': 'Create New Task'
    }
    return render(request, 'todo/task_form.html', context)


@login_required
def task_update(request, pk):
    """Update existing task"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated successfully!')
            return redirect('todo:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form,
        'task': task,
        'title': 'Edit Task'
    }
    return render(request, 'todo/task_form.html', context)


@login_required
def task_delete(request, pk):
    """Delete task"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" deleted successfully!')
        return redirect('todo:task_list')
    
    context = {
        'task': task
    }
    return render(request, 'todo/task_confirm_delete.html', context)


@login_required
def task_toggle_complete(request, pk):
    """Toggle task completion status"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if task.status == 'completed':
        task.mark_incomplete()
        messages.success(request, f'Task "{task.title}" marked as incomplete.')
    else:
        task.mark_complete()
        messages.success(request, f'Task "{task.title}" marked as complete!')
    
    # Redirect back to referring page
    next_url = request.GET.get('next', 'todo:task_list')
    return redirect(next_url)


@login_required
def task_update_status(request, pk):
    """Quick update task status"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            if new_status == 'completed':
                task.completed_date = timezone.now()
            else:
                task.completed_date = None
            task.save()
            messages.success(request, f'Task status updated to {task.get_status_display()}!')
    
    return redirect('todo:task_list')


@login_required
def task_bulk_delete(request):
    """Bulk delete completed tasks"""
    if request.method == 'POST':
        deleted_count = Task.objects.filter(
            user=request.user,
            status='completed'
        ).delete()[0]
        
        messages.success(request, f'Deleted {deleted_count} completed task(s)!')
    
    return redirect('todo:task_list')