from django.contrib import admin
from django.urls import path
from .views import Index, About_us, Dashboard, SignUpView, AddItem, EditItem, DeleteItem
from django.contrib.auth import views as auth_views
#from django.contrib.auth.views import LogoutView
from .views import custom_logout

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('about_us/', About_us.as_view(), name='about_us'),  
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='bee_inventory/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='bee_inventory/logout.html'), name='logout'),
    path('logout/', custom_logout, name='logout'),
]