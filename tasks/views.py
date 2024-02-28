from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from . import models


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'users_count': models.get_user_model().objects.count(),
        'plans_count': models.Plan.objects.count(),
        'tasks_count': models.Task.objects.count(),
    }
    return render(request, 'tasks/index.html', context)

def task_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'tasks/task_list.html', {
        'task_list': models.Task.objects.all(),
    })

def task_detail(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'tasks/task_detail.html', {
        'task': get_object_or_404(models.Task, pk=pk),
    })

def task_done(request: HttpRequest, pk:int) -> HttpResponse:
    task = get_object_or_404(models.Task, pk=pk)
    task.is_done = not task.is_done
    task.save()
    messages.success(request, "{} {} {} {}".format(
        _('task').capitalize(),
        task.name,
        _('marked as'),
        _('done') if task.is_done else _('undone'),
    ))
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect(task_list)
