from django.db import models


class OrderableQueryset(models.QuerySet):
    """
    Adds additional functionality to `Orderable.objects` and querysets.

    Provides access to the next and previous ordered object within the queryset.

    As a related manager this will provide the filtering automatically. Should you wish
    to
    """
    def before(self, orderable):
        return self.filter(sort_order__lt=orderable.sort_order).last()

    def after(self, orderable):
        return self.filter(sort_order__gt=orderable.sort_order).first()
