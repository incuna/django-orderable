from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, models, transaction

from .managers import OrderableManager


class Orderable(models.Model):
    """
    An orderable object that keeps all the instances in an enforced order.

    If there's a unique_together which includes the sort_order field then that
    will be used when checking for collisions etc.

    This works well for inlines, which can be manually reordered by entering
    numbers, and the save function will prevent against collisions.

    For main objects, you would want to also use "OrderableAdmin", which will
    make a nice jquery admin interface.
    """
    sort_order = models.IntegerField(blank=True, db_index=True)

    objects = OrderableManager()

    class Meta:
        abstract = True
        ordering = ['sort_order']

    def get_unique_fields(self):
        """List field names that are unique_together with `sort_order`."""
        for unique_together in self._meta.unique_together:
            if 'sort_order' in unique_together:
                unique_fields = list(unique_together)
                unique_fields.remove('sort_order')
                return ['%s_id' % f for f in unique_fields]
        return []

    def get_filtered_manager(self):
        manager = self.__class__.objects
        kwargs = {field: getattr(self, field) for field in self.get_unique_fields()}
        return manager.filter(**kwargs)

    def next(self):
        if not self.sort_order:
            return None

        return self.get_filtered_manager().after(self)

    def prev(self):
        if not self.sort_order:
            return None

        return self.get_filtered_manager().before(self)

    @staticmethod
    def _update(qs):
        """
        Increment the sort_order in a queryset.

        Handle IntegrityErrors caused by unique constraints.
        """
        try:
            with transaction.atomic():
                qs.update(sort_order=models.F('sort_order') + 1)
        except IntegrityError:
            for obj in qs.order_by('-sort_order'):
                qs.filter(pk=obj.pk).update(sort_order=models.F('sort_order') + 1)

    def _save(self, objects, old_pos, new_pos):
        """WARNING: Intensive giggery-pokery zone."""
        to_shift = objects.exclude(pk=self.pk) if self.pk else objects

        # If not set, insert at end.
        if self.sort_order is None:
            self._move_to_end(objects)

        # New insert.
        elif not self.pk and not old_pos:
            # Increment `sort_order` on objects with:
            #     sort_order > new_pos.
            to_shift = to_shift.filter(sort_order__gte=self.sort_order)
            self._update(to_shift)
            self.sort_order = new_pos

        # self.sort_order decreased.
        elif old_pos and new_pos < old_pos:
            self._move_to_end(objects)
            super(Orderable, self).save()
            # Increment `sort_order` on objects with:
            #     sort_order >= new_pos and sort_order < old_pos
            to_shift = to_shift.filter(sort_order__gte=new_pos, sort_order__lt=old_pos)
            self._update(to_shift)
            self.sort_order = new_pos

        # self.sort_order increased.
        elif old_pos and new_pos > old_pos:
            self._move_to_end(objects)
            super(Orderable, self).save()
            # Decrement sort_order on objects with:
            #     sort_order <= new_pos and sort_order > old_pos.
            to_shift = to_shift.filter(sort_order__lte=new_pos, sort_order__gt=old_pos)
            to_shift.update(sort_order=models.F('sort_order') - 1)
            self.sort_order = new_pos

    def _move_to_end(self, objects):
        """Temporarily save `self.sort_order` elsewhere (max_obj)."""
        max_obj = objects.all().aggregate(models.Max('sort_order'))['sort_order__max']
        self.sort_order = max_obj + 1 if max_obj else 1

    def _unique_togethers_changed(self):
        for field in self.get_unique_fields():
            if getattr(self, '_original_%s' % field, False):
                return True
        return False

    def save(self, *args, **kwargs):
        """Keep the unique order in sync."""
        objects = self.get_filtered_manager()
        old_pos = getattr(self, '_original_sort_order', None)
        new_pos = self.sort_order

        if old_pos is None and self._unique_togethers_changed():
            self.sort_order = None
            new_pos = None

        try:
            with transaction.atomic():
                self._save(objects, old_pos, new_pos)
        except IntegrityError:
            with transaction.atomic():
                old_pos = objects.filter(pk=self.pk).values_list(
                    'sort_order', flat=True)[0]
                self._save(objects, old_pos, new_pos)

        # Call the "real" save() method.
        super(Orderable, self).save(*args, **kwargs)

    def sort_order_display(self):
        template = '<span id="neworder-{}" class="sorthandle">{}</span>'
        return template.format(self.id, self.sort_order)
    sort_order_display.allow_tags = True
    sort_order_display.short_description = 'Order'
    sort_order_display.admin_order_field = 'sort_order'

    def __setattr__(self, attr, value):
        """
        Cache original value of `sort_order` when a change is made to it.

        Also cache values of other unique together fields.

        Greatly inspired by http://code.google.com/p/django-audit/
        """
        if attr == 'sort_order' or attr in self.get_unique_fields():
            try:
                current = self.__dict__[attr]
            except (AttributeError, KeyError, ObjectDoesNotExist):
                pass
            else:
                previously_set = getattr(self, '_original_%s' % attr, False)
                if current != value and not previously_set:
                    setattr(self, '_original_%s' % attr, current)
        super(Orderable, self).__setattr__(attr, value)
