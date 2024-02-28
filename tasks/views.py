from typing import Any
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from . import models


class PlanListView(generic.ListView):
    model = models.Plan
    template_name = 'tasks/plan_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if self.request.GET.get('owner'):
            queryset = queryset.filter(owner__username=self.request.GET.get('owner'))
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_list'] = get_user_model().objects.all()
        return context


class PlanDetailView(generic.DetailView):
    model = models.Plan
    template_name = 'tasks/plan_detail.html'


class PlanCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Plan
    template_name = 'tasks/plan_create.html'
    fields = ('name', )

    def get_success_url(self) -> str:
        messages.success(self.request, 
            _('plan created succesfully').capitalize())
        return reverse('plan_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PlanUpdateView(LoginRequiredMixin,
        UserPassesTestMixin,
        generic.UpdateView,
    ):
    model = models.Plan
    template_name = 'tasks/plan_update.html'
    fields = ('name', )

    def get_success_url(self) -> str:
        messages.success(self.request, 
            _('plan updated succesfully').capitalize())
        return reverse('plan_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user or self.request.user.is_superuser


class PlanDeleteView(LoginRequiredMixin,
        UserPassesTestMixin,
        generic.DeleteView,
    ):
    model = models.Plan
    template_name = 'tasks/plan_delete.html'

    def get_success_url(self) -> str:
        messages.success(self.request, 
            _('plan deleted succesfully').capitalize())
        return reverse('plan_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user or self.request.user.is_superuser


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'users_count': models.get_user_model().objects.count(),
        'plans_count': models.Plan.objects.count(),
        'tasks_count': models.Task.objects.count(),
    }
    return render(request, 'tasks/index.html', context)

def task_list(request: HttpRequest) -> HttpResponse:

    queryset = models.Task.objects
    owner_username = request.GET.get('owner')
    if owner_username:
        owner = get_object_or_404(get_user_model(), username=owner_username)
        queryset = queryset.filter(owner=owner)
        plans = models.Plan.objects.filter(owner=owner)
    else:
        plans = models.Plan.objects.all()
    plan_pk = request.GET.get('plan')
    if plan_pk:
        plan = get_object_or_404(models.Plan, pk=plan_pk)
        queryset = queryset.filter(plan=plan)
    search_name = request.GET.get('search_name')
    if search_name:
        queryset = queryset.filter(name__icontains=search_name)
    context = {
        'task_list': queryset.all(),
        'plan_list': plans,
        'user_list': get_user_model().objects.all().order_by('username')
    }
    return render(request, 'tasks/task_list.html', context)


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
