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

    def set_orders(self, object_pks):
        """
        Perform a mass update of sort_orders across the full queryset.
        Accepts a list, object_pks, of the intended order for the objects.

        Works as follows:
        - Compile a list of all sort orders in the queryset. Leave out anything that
          isn't in the object_pks list - this deals with pagination and any
          inconsistencies.
        - Get the maximum among all model object sort orders. Update the queryset to add
          it to all the existing sort order values. This lifts them 'out of the way' of
          unique_together clashes when setting the intended sort orders.
        - Set the sort order on each object. Use only sort_order values that the objects
          had before calling this method, so they get rearranged in place.
        Performs O(n) queries.
        """
        objects_to_sort = self.filter(pk__in=object_pks)
        max_value = self.model.objects.all().aggregate(
            models.Max('sort_order')
        )['sort_order__max']

        # Call list() on the values right away, so they don't get affected by the
        # update() later (since values_list() is lazy).
        orders = list(objects_to_sort.values_list('sort_order', flat=True))

        # Check there are no unrecognised entries in the object_pks list. If so,
        # throw an error. We only have to check that they're the same length because
        # orders is built using only entries in object_pks, and all the pks are unique,
        # so if their lengths are the same, the elements must match up exactly.
        if len(orders) != len(object_pks):
            pks = set(objects_to_sort.values_list('pk', flat=True))
            message = 'The following object_pks are not in this queryset: {}'.format(
                [pk for pk in object_pks if pk not in pks]
            )
            raise TypeError(message)

        with transaction.atomic():
            objects_to_sort.update(sort_order=models.F('sort_order') + max_value)
            for pk, order in zip(object_pks, orders):
                # Use update() to save a query per item and dodge the insertion sort
                # code in save().
                self.filter(pk=pk).update(sort_order=order)

        # Return the operated-on queryset for convenience.
        return objects_to_sort
