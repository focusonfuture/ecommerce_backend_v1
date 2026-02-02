from django.urls import path
from . import views
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', admin_login_view, name='admin_login'),
    path('admin/logout/', views.admin_logout_view, name='admin_logout'),
    path('admin/', admin_home_view, name='admin_home'),       
    path('admin/dashboard/', admin_home_view, name='admin_dashboard'),  
]