v6.0.1
======

* Add Django 2.1 to TravisCI build
* Fix edit inline issues causing reordering to fail when items have equal sort_order values.

v6.0.0
======

* Drop support for django 1.10 and below. Things probably still work on the old versions, we're just no longer supporting them.
* Drop support for Python 3.3. Again, it probably still works, just not supported.
* Add django 2.0 support (nothing significant actually changed -- only tests).
* Fix `sort_order_display` in Django admin change_list view.

v5.0.0
======

* Drop support for django versions before 1.8.
* Add `before` and `after` to `OrderableQueryset` to return the next item in the set.
    - example usage: `ordered_queryset.objects.after(ordered_object)`
* Add `OrderableQueryset.set_orders()` to perform a mass rearrangement of items. This now requires custom model managers to inherit from `OrderableManager`.
* Add `_pass_through_save()` to `Orderable`. This allows you to skip the insertion sorting performed by the `save()` method, such as when updating multiple objects at once to rearrange them. (`set_orders()` uses it.)

v4.0.5
======

* Use `attr` to set input field values in the DOM instead of `val`, fixing the drag/drop behaviour.

v4.0.4
======

* (Also) use `{% static %}` instead of `{{ STATIC_URL }}` to display the drag handle image in the orderable_tabular.html.

v4.0.3
======

* Use `{% static %}` instead of `{{ STATIC_URL }}` to display the drag handle image.

v4.0.2
======

* Fix `IntegrityError` in `Orderable.save` when `sort_order` has a `unique` constraint.

v4.0.1
======

* Fix jQuery (and UI) missing from OrderableTabularInline.

v4.0.0
======

* Drop support for Django versions less than 1.6.
* Prevent integrity errors with unique_together conditions containing sort_order.

v3.1.0
======

* Default to hosted jQuery and jQuery UI from google CDN. `\o/`

v3.0.0
======

* Drop support for django 1.5 and python 2.6.
* Add (preliminary) support for django 1.7 and python 3.4.
* Code quality related refactor.


v2.0.3
======

* Accept zero as a valid value for sort_order

v2.0.2
======

* Use model_name instead of deprecated module_name in django >= 1.6

v2.0.1
======

* Added tests to `Orderable.save`
* Removed `django.db.transation.atomic` from the save method in django 1.6.
* Reduced number of queries on insert of new `Orderable`.

v2.0.0
======

* Don't use `commit_on_success` in model save.

**Warning** Potentially backwards incompatible. We have removed this feature
because it can cause database transactions to be commited that would
otherwise have been rolled back.

We recommend you make sure to use 'django.middleware.transaction.TransactionMiddleware', or at least use `django.db.transaction.commit_on_success` on any code that invokes the save method as it would otherwise be vulnerable to race conditions. If you are on django 1.6 we would instead recommend setting `settings.ATOMIC_REQUESTS = True`.

This version added `django.db.transation.atomic` to `Orderable.save` method
(in django 1.6 only) but it was immediately removed in `2.0.1`.

v1.2.0
======

* Don't patch `__setattr__` for everything

v1.1.1
======

* Don't fall over on KeyError.

v1.1
====

* Refactor database code for better efficiency/lower collisions.
* Add `db_index=True` to `sort_order` field.
* Fix `OrderableTabularInline`.
