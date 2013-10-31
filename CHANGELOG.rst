v2.0.0
======

* Don't use `commit_on_success` in model save.

**Warning:** Potentially backwards incompatible. We have removed this feature
  because it can cause database transactions to be commited that would
  otherwise have been rolled back.

  If you're using Django 1.6+ we have wrapped the save method in
  `django.db.transaction.atomic` for you (but you are using `ATOMIC_REQUESTS`,
  right?). Otherwise, we recommend you make sure to use
  'django.middleware.transaction.TransactionMiddleware', or at least use
  `django.db.transaction.commit_on_success` on any code that invokes the save
  method as it would otherwise be vulnerable to race conditions.

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
