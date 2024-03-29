from .models import ViewCount
from modules.services.utils import get_client_ip
from datetime import timedelta
from django.utils import timezone


class ViewCountMixin:
    """
    Миксин для увеличения счетчика просмотров статьи
    """
    def get_object(self):
        # получаем статью по заданному slug
        obj = super().get_object()
        # получаем IP-адрес пользователя и ключ сессии
        ip_address = get_client_ip(self.request)
        # получаем текущую дату и время
        now = timezone.now()
        # вычитаем 7 дней из текущей даты
        week_ago = now - timedelta(days=1)
        # проверяем, есть ли записи за последние 7 дней для данного пользователя и данной статьи
        # если нет, то создаем новую запись
        ViewCount.objects.get_or_create(article=obj, ip_address=ip_address, viewed_on__gte=week_ago)
        return obj