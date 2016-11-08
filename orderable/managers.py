from django.db.models import manager

from .querysets import OrderableQueryset


class OrderableManager(manager.BaseManager.from_queryset(OrderableQueryset)):
    pass
