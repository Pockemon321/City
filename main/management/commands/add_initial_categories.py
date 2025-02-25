from django.core.management.base import BaseCommand
from main.models import Category

class Command(BaseCommand):
    help = 'Adds initial categories to the database'

    def handle(self, *args, **kwargs):
        categories = [
            'Дороги и тротуары',
            'Освещение',
            'Детские площадки',
            'Озеленение',
            'Уборка территории',
            'Коммунальные услуги',
            'Общественный транспорт',
            'Парковки',
            'Вывоз мусора',
            'Благоустройство дворов',
        ]

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully added category "{category_name}"'))
