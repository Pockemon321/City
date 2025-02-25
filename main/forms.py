from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Request, Category

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        validators=[RegexValidator(
            regex=r'^[а-яА-ЯёЁ\s-]+$',
            message='ФИО может содержать только кириллические буквы, пробелы и дефис'
        )],
        label='Полное имя'
    )
    email = forms.EmailField(label='Email')
    agreement = forms.BooleanField(
        required=True,
        label='Я согласен с условиями использования'
    )

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Логин',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isascii():
            raise forms.ValidationError('Логин должен содержать только латинские буквы')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Этот логин уже занят')
        return username

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'category', 'before_image']
        widgets = {
            'before_image': forms.FileInput(attrs={'accept': '.jpg,.jpeg,.png,.bmp'})
        }

    def clean_before_image(self):
        image = self.cleaned_data.get('before_image')
        if image:
            if image.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError('Размер файла не должен превышать 10МБ')
        return image

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Название категории'
        }

class RequestStatusForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['status', 'after_image', 'rejection_reason']
        widgets = {
            'after_image': forms.FileInput(attrs={'accept': '.jpg,.jpeg,.png,.bmp'})
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        after_image = cleaned_data.get('after_image')
        rejection_reason = cleaned_data.get('rejection_reason')

        if status == 'solved' and not after_image:
            raise forms.ValidationError('При решении проблемы необходимо прикрепить фото')
        
        if status == 'rejected' and not rejection_reason:
            raise forms.ValidationError('При отклонении заявки необходимо указать причину')
