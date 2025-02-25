from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-solved-count/', views.get_solved_count, name='get_solved_count'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='main/logout.html',
        next_page='home',
        http_method_names=['get', 'post']
    ), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('delete-request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('category-management/', views.category_management, name='category_management'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
]
