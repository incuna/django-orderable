from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db import transaction


class Orderable(models.Model):
    """An orderable object that keeps all the instances in an enforced order
    If there's a unique_together which includes the sort_order field then that
    will be used when checking for collisions etc.

    This works well for inlines, which can be manually reordered by entering
    numbers, and the save function will prevent against collisions.

    For main objects, you would want to also use "OrderableAdmin", which will
    make a nice jquery admin interface.
    """
    sort_order = models.IntegerField(blank=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['sort_order']

    def get_unique_fields(self):
        """Fetches a list of field names that are set as unique with the sort order."""
        for unique_together in self._meta.unique_together:
            # for together in togethers:
            if 'sort_order' in unique_together:
                unique_fields = list(unique_together)
                unique_fields.remove('sort_order')
                return unique_fields

    def get_filters(self):
        """Builds a dictionary of kwargs that can be used to select unique-together records."""
        unique_fields = self.get_unique_fields()
        if unique_fields:
            kwargs = {}
            for field in unique_fields:
                kwargs[field] = getattr(self, field)
            return kwargs

    def get_filtered_manager(self):
        """
        Returns the appropriate manager which may already have a filter
        applied based on the unique_together.
        """
        obj = type(self)
        extra_kwargs = self.get_filters()
        if extra_kwargs:
            return obj.objects.filter(**extra_kwargs)
        return obj.objects

    def next(self):
        if not self.sort_order:
            return None
        objects = self.get_filtered_manager()
        try:
            return objects.filter(sort_order__gt=self.sort_order).order_by('sort_order')[0]
        except IndexError:
            return None

    def prev(self):
        if not self.sort_order:
            return None
        objects = self.get_filtered_manager()
        try:
            return objects.filter(sort_order__lt=self.sort_order).order_by('-sort_order')[0]
        except IndexError:
            return None

    @transaction.commit_on_success()
    def save(self, *args, **kwargs):
        """
        Keep the unique order in sync.

        In transaction to avoid race conditions.

        WARNING: Intensive giggery-pokery zone.
        """
        objects = self.get_filtered_manager()
        to_shift = objects.exclude(pk=self.pk) if self.pk else objects
        old_pos = getattr(self, '_original_sort_order', None)
        new_pos = self.sort_order

        def _move_to_end(commit=True):
            """Temporarily save `self.sort_order` elsewhere (max_obj)."""
            max_obj = objects.all().aggregate(models.Max('sort_order'))['sort_order__max']
            self.sort_order = max_obj + 1 if max_obj else 1  # May be overwritten later.
            if commit:
                super(Orderable, self).save(*args, **kwargs)

        def _move_back():
            """Reset the position of `self.sort_order` before saving."""
            self.sort_order = new_pos

        # If not set, insert at end.
        if not self.sort_order:
            _move_to_end(commit=False)

        # New insert.
        elif not self.pk and not old_pos:
            _move_to_end()
            # Increment `sort_order` on objects with:
            #     sort_order > new_pos.
            to_shift = to_shift.filter(sort_order__gte=self.sort_order)
            to_shift.update(sort_order=models.F('sort_order') + 1)
            _move_back()

        # self.sort_order decreased.
        elif new_pos < old_pos:
            _move_to_end()
            # Increment `sort_order` on objects with:
            #     sort_order >= new_pos and sort_order < old_pos
            to_shift = to_shift.filter(sort_order__gte=new_pos, sort_order__lt=old_pos)
            to_shift.update(sort_order=models.F('sort_order') + 1)
            _move_back()

        # self.sort_order increased.
        elif old_pos and new_pos > old_pos:
            _move_to_end()
            # Decrement sort_order on objects with:
            #     sort_order <= new_pos and sort_order > old_pos.
            to_shift = to_shift.filter(sort_order__lte=new_pos, sort_order__gt=old_pos)
            to_shift.update(sort_order=models.F('sort_order') - 1)
            _move_back()

        # Call the "real" save() method.
        super(Orderable, self).save(*args, **kwargs)

    def sort_order_display(self):
        return "<span id='neworder-%s' class='sorthandle'>%s</span>" % (self.id, self.sort_order)
    sort_order_display.allow_tags = True
    sort_order_display.short_description = 'Order'
    sort_order_display.admin_order_field = 'sort_order'

    def __setattr__(self, attr, value):
        """
        When a change is made to the `sort_order`, save the original value.

        Greatly inspired by http://code.google.com/p/django-audit/
        """
        try:
            current = getattr(self, attr)
        except (AttributeError, KeyError, ObjectDoesNotExist):
            pass
        else:
            if attr == 'sort_order' and current != value and not getattr(self, '_original_sort_order', False):
                self._original_sort_order = current
        super(Orderable, self).__setattr__(attr, value)
