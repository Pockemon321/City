from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .forms import UserRegisterForm, RequestForm, RequestStatusForm, CategoryForm
from .models import Request, Category
import bleach

def is_admin(user):
    return user.is_staff

def sanitize_html(text):
    """Очистка HTML от потенциально опасных тегов и атрибутов"""
    allowed_tags = ['p', 'b', 'i', 'u', 'em', 'strong', 'br']
    allowed_attributes = {}
    return bleach.clean(text, tags=allowed_tags, attributes=allowed_attributes)

@require_http_methods(["GET"])
def home(request):
    solved_requests = Request.objects.filter(status='solved').order_by('-created_date')[:4]
    solved_count = Request.objects.filter(status='solved').count()
    return render(request, 'main/index.html', {
        'solved_requests': solved_requests,
        'solved_count': solved_count
    })

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data.get('full_name')
            user.save()
            messages.success(request, 'Аккаунт успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.user = request.user
            
            # Очистка описания от потенциально опасного HTML
            request_obj.description = sanitize_html(request_obj.description)
            
            request_obj.save()
            messages.success(request, 'Заявка успешно отправлена!')
            return redirect('profile')
    else:
        form = RequestForm()
    
    user_requests = Request.objects.filter(user=request.user)
    categories = Category.objects.all()
    
    return render(request, 'main/profile.html', {
        'form': form,
        'requests': user_requests,
        'categories': categories
    })

@login_required
@require_http_methods(["POST"])
def delete_request(request, request_id):
    try:
        user_request = Request.objects.get(id=request_id, user=request.user)
        if user_request.status == 'new':
            user_request.delete()
            messages.success(request, 'Заявка успешно удалена')
        else:
            messages.error(request, 'Нельзя удалить заявку, которая уже обработана')
    except Request.DoesNotExist:
        messages.error(request, 'Заявка не найдена')
    return redirect('profile')

@user_passes_test(is_admin)
@require_http_methods(["GET"])
def admin_dashboard(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        try:
            request_obj = Request.objects.get(id=request_id)
            form = RequestStatusForm(request.POST, request.FILES, instance=request_obj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Статус заявки успешно обновлен!')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
        except Request.DoesNotExist:
            messages.error(request, 'Заявка не найдена')
        return redirect('admin_dashboard')

    requests = Request.objects.all().order_by('-created_date')
    categories = Category.objects.all()
    return render(request, 'main/admin_dashboard.html', {
        'requests': requests,
        'categories': categories
    })

@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def category_management(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно добавлена!')
            return redirect('category_management')
    else:
        form = CategoryForm()

    categories = Category.objects.all()
    return render(request, 'main/category_management.html', {
        'form': form,
        'categories': categories
    })

@user_passes_test(is_admin)
@require_http_methods(["POST"])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, 'Категория успешно удалена')
    except Category.DoesNotExist:
        messages.error(request, 'Категория не найдена')
    return redirect('category_management')

@login_required
@require_http_methods(["GET"])
def get_solved_count(request):
    count = Request.objects.filter(status='solved').count()
    return JsonResponse({'count': count})
