from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('plans/', views.PlanListView.as_view(), name='plan_list'),
     path('plans/create', views.PlanCreateView.as_view(), name='plan_create'),
     path('plan/<int:pk>/', views.PlanDetailView.as_view(), name='plan_detail'),
     path('plan/<int:pk>/edit/', views.PlanUpdateView.as_view(), name='plan_update'),
     path('plan/<int:pk>/delete/', views.PlanDeleteView.as_view(), name='plan_delete'),
     path('tasks/', views.task_list, name='task_list'),
     path('task/<int:pk>/', views.task_detail, name='task_detail'),
     path('task/<int:pk>/done/', views.task_done, name='task_done'),
]