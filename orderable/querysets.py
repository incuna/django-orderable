from django.db import models, transaction


class OrderableQueryset(models.QuerySet):
    """
    Adds additional functionality to `Orderable.objects` and querysets.

    Provides access to the next and previous ordered object within the queryset.

    As a related manager this will provide the filtering automatically.
    """
    def before(self, orderable):
        return self.filter(sort_order__lt=orderable.sort_order).last()

    def after(self, orderable):
        return self.filter(sort_order__gt=orderable.sort_order).first()

    def set_orders(self, object_pks, *args, **kwargs):
        """
        Perform a mass update of sort_orders across the full queryset.
        Accepts a list, object_pks, of the intended order for the objects.

        Works as follows:
        - Compile a list of all sort orders in the queryset.
        - Get the maximum among all model object sort orders. Update the queryset to add
          it to all the existing sort order values. This lifts them 'out of the way' of
          unique_together clashes when setting the intended sort orders.
        - Set the sort order on each object.
        Performs O(n) queries.
        """
        orders = self.values_list('sort_order', flat=True)  # will be sorted
        print(orders)
        if len(object_pks) != len(orders):
            raise TypeError(
                'A list of object pks supplied to OrderableQueryset.set_orders() must ' +
                'be of the same length as the queryset itself.'
            )

        max_value = self.model.objects.count()
        self.update(sort_order=models.F('sort_order') + max_value)

        with transaction.atomic():
            for i, pk in enumerate(object_pks):
                obj = self.get(pk=pk)
                obj.sort_order = orders[i]
                obj._pass_through_save()

        # Return the operated-on queryset for convenience.
        return self
