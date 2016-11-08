from django.db.models import Manager

from .querysets import OrderableQueryset


class OrderableManager(Manager.from_queryset(OrderableQueryset)):
    pass
