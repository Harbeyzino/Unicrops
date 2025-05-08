from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Project, Task, SubTask, TaskProgress, Comment, Notification
from .forms import TaskForm, SubTaskForm, ProgressForm, CommentForm
from django.utils import timezone
from datetime import timedelta

@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            
            # Calculate end date based on time frame
            time_value = form.cleaned_data['time_value']
            time_unit = form.cleaned_data['time_unit']
            
            if time_unit == 'H':
                task.end_date = timezone.now() + timedelta(hours=time_value)
            elif time_unit == 'D':
                task.end_date = timezone.now() + timedelta(days=time_value)
            elif time_unit == 'W':
                task.end_date = timezone.now() + timedelta(weeks=time_value)
            elif time_unit == 'M':
                task.end_date = timezone.now() + timedelta(days=time_value*30)  # Approximate
            elif time_unit == 'Y':
                task.end_date = timezone.now() + timedelta(days=time_value*365)  # Approximate
            
            task.save()
            
            # Create notification for assigned user
            if task.assigned_to:
                Notification.objects.create(
                    user=task.assigned_to,
                    message=f"You have been assigned a new task: {task.title}",
                    link=f"/tasks/{task.id}/"
                )
            
            messages.success(request, 'Task created successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()
    
    return render(request, 'tasks/create_task.html', {'form': form, 'project': project})

@login_required
def add_subtask(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = SubTaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.task = task
            subtask.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = SubTaskForm()
    
    return render(request, 'tasks/add_subtask.html', {'form': form, 'task': task})

@login_required
def update_progress(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = ProgressForm(request.POST, request.FILES)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.task = task
            progress.created_by = request.user
            
            if progress.status == 'completed':
                task.is_completed = True
                task.save()
            
            progress.save()
            
            # Create notification for admin/project owner
            Notification.objects.create(
                user=task.project.client,
                message=f"Progress update on task: {task.title}",
                link=f"/tasks/{task.id}/"
            )
            
            messages.success(request, 'Progress updated successfully!')
            return redirect('task_detail', task_id=task.id)
    else:
        form = ProgressForm()
    
    return render(request, 'tasks/update_progress.html', {'form': form, 'task': task})

@login_required
def add_comment(request, progress_id):
    progress = get_object_or_404(TaskProgress, id=progress_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.progress = progress
            comment.user = request.user
            comment.save()
            
            # Notify other participants
            participants = set()
            participants.add(progress.task.assigned_to)
            participants.add(progress.task.created_by)
            participants.add(progress.task.project.client)
            
            for user in participants:
                if user and user != request.user:
                    Notification.objects.create(
                        user=user,
                        message=f"New comment on task: {progress.task.title}",
                        link=f"/tasks/{progress.task.id}/"
                    )
            
            return redirect('task_detail', task_id=progress.task.id)
    else:
        form = CommentForm()
    
    return render(request, 'tasks/add_comment.html', {'form': form, 'progress': progress})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    progress_updates = task.progress_updates.all().order_by('-created_at')
    subtasks = task.subtasks.all()
    
    # Calculate progress percentage
    total_duration = (task.end_date - task.start_date).total_seconds()
    elapsed_time = (timezone.now() - task.start_date).total_seconds()
    
    if total_duration > 0:
        time_progress = min(100, (elapsed_time / total_duration) * 100)
    else:
        time_progress = 0
    
    # Calculate completion percentage based on subtasks
    if subtasks.exists():
        completed_subtasks = subtasks.filter(is_completed=True).count()
        subtask_progress = (completed_subtasks / subtasks.count()) * 100
    else:
        subtask_progress = 0
    
    # Overall progress (average of time and subtask progress)
    if task.is_completed:
        overall_progress = 100
    else:
        overall_progress = (time_progress + subtask_progress) / 2
    
    comment_form = CommentForm()
    
    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'progress_updates': progress_updates,
        'subtasks': subtasks,
        'overall_progress': overall_progress,
        'comment_form': comment_form,
    })

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})