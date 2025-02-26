from django.core.cache import cache
from django.http import HttpResponseForbidden

class LoginRateThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/login/' and request.method == 'POST':
            ip = request.META.get('REMOTE_ADDR')
            key = f'login_attempts_{ip}'
            attempts = cache.get(key, 0)

            if attempts >= 5:  # Максимум 5 попыток
                return HttpResponseForbidden('Слишком много попыток входа. Попробуйте позже.')
            
            cache.set(key, attempts + 1, 300)  # Блокировка на 5 минут

        response = self.get_response(request)
        return response
