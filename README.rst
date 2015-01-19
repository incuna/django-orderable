django-orderable
================

Make models orderable in the Admin.

Included:

* Abstract base Model
* Admin class
* Inline admin class
* Admin templates


Installation
------------

Grab from the PyPI: ::

    pip install django-orderable


Add to your INSTALLED_APPS: ::

    ...
    'orderable',
    ...

Subclass the Orderable class: ::

    from orderable.models import Orderable


    class Book(Orderable):
        ...


**Note:** If your subclass of Orderable has a Metaclass then make sure it subclasses the Orderable one so the model is sorted by ``sort_order``.

** *Also* Note:** Saving orderable models invokes a fair number of queries and
in order to avoid race conditions should be run in a transaction. If you're
using django >= 1.6 we recommend you set `DATABASES['default']['ATOMIC_REQUESTS'] = True` in your
settings, if you're not yet on django 1.6, we recommend use of
`TransactionMiddleware`.


Subclass the appropriate Orderable admin classes: ::

    from orderable.admin import OrderableAdmin, OrderableTabularInline


    class SomeInlineClass(OrderableTabularInline):
        ...

    class SomeAdminClass(OrderableAdmin):
        list_display = ('__unicode__', 'sort_order_display')
        ...


jQuery and jQuery UI are used in the Admin for the actual moveable UI. You may override the versions with your own (rather than using the google cdn)::

    class SomeAdminClass(OrderableAdmin):
        class Media:
            js = (
                'path/to/jquery.js',
                'path/to/jquery.ui.js',
            )


Common Gotchas
--------------

Adding Orderable to Existing Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need to populate the required `sort_order` field. Typically this is done by adding the
field in one migration with a default of `0`, then creating a data migration to set the value to
that of its primary key::

    for obj in orm['appname.Model'].objects.all():
        obj.sort_order = obj.pk
        obj.save()


Multiple Models using Orderable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When multiple models inherit from Orderable the `next()` and `previous()` methods will look for the
next/previous model with a sort order. However you'll likely want to have the various sort orders
determined by a foreign key or some other predicate. The easiest way (currently) is to override the
method in question.
