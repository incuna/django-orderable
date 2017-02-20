from django.db.models import Manager

from .querysets import OrderableQueryset


"""
A manager for Orderables. If you customise your model's manager, be sure to inherit from
this rather than django.db.models.Manager; it's required for the drag/drop ordering
to work in the admin.
"""
OrderableManager = Manager.from_queryset(OrderableQueryset)
