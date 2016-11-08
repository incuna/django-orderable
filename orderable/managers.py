from django.db.models import manager

from .querysets import OrderableQueryset


OrderableManager = manager.BaseManager.from_queryset(OrderableQueryset)
