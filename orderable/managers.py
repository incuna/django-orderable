from django.db import models


class OrderableManager(models.Manager):
    '''
    Adds additional functionality to `Orderable.objects` providing access to the next and
    previous ordered object within the queryset.
    '''
    def before(self, orderable):
        return self.filter(sort_order__lt=orderable.sort_order).last()

    def after(self, orderable):
        return self.filter(sort_order__gt=orderable.sort_order).first()
