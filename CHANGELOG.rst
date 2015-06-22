v4.0.0
======

* Dropped support for Django versions less than 1.5.
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
