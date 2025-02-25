from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import UserRegisterForm, RequestForm, RequestStatusForm, CategoryForm
from .models import Request, Category
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    solved_requests = Request.objects.filter(status='solved').order_by('-created_date')[:4]
    solved_count = Request.objects.filter(status='solved').count()
    return render(request, 'main/index.html', {
        'solved_requests': solved_requests,
        'solved_count': solved_count
    })

def get_solved_count(request):
    count = Request.objects.filter(status='solved').count()
    return JsonResponse({'count': count})

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
def profile(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.user = request.user
            request_obj.save()
            messages.success(request, 'Ваша заявка успешно отправлена!')
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

@staff_member_required
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

@staff_member_required
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

@staff_member_required
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, 'Категория успешно удалена')
    except Category.DoesNotExist:
        messages.error(request, 'Категория не найдена')
    return redirect('category_management')
