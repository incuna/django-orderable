from django.db.models import Manager

from .querysets import OrderableQueryset


OrderableManager = Manager.from_queryset(OrderableQueryset)
