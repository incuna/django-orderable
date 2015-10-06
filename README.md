# Django Orderable


Add manual sort order to Django objects via an abstract base class and admin classes. Project includes:

* Abstract base Model
* Admin class
* Inline admin class
* Admin templates


## Demo


![django-orderable demo](https://cloud.githubusercontent.com/assets/30606/6326221/667992e0-bb47-11e4-923e-29334573ff5c.gif)

## Installation


Grab from the PyPI:

    pip install django-orderable


Add to your INSTALLED_APPS:

    ...
    'orderable',
    ...

Subclass the Orderable class:

    from orderable.models import Orderable


    class Book(Orderable):
        ...

Subclass the appropriate Orderable admin classes:

    from orderable.admin import OrderableAdmin, OrderableTabularInline


    class SomeInlineClass(OrderableTabularInline):
        ...

    class SomeAdminClass(OrderableAdmin):
        list_display = ('__unicode__', 'sort_order_display')
        ...


jQuery and jQuery UI are used in the Admin for the draggable UI. You may override the versions with your own (rather than using Google's CDN):

    class SomeAdminClass(OrderableAdmin):
        class Media:
            extend = False
            js = (
                'path/to/jquery.js',
                'path/to/jquery.ui.js',
            )


## Notes

### Metaclasses

If your subclass of Orderable has a Metaclass then make sure it subclasses the Orderable one so the model is sorted by ``sort_order``.

### Transactions

Saving orderable models invokes a fair number of database queries, and in order
to avoid race conditions should be run in a transaction.

### Adding Orderable to Existing Models

You will need to populate the required `sort_order` field. Typically this is
done by adding the field in one migration with a default of `0`, then creating
a data migration to set the value to that of its primary key:


    for obj in orm['appname.Model'].objects.all():
        obj.sort_order = obj.pk
        obj.save()


### Multiple Models using Orderable

When multiple models inherit from Orderable the `next()` and `previous()`
methods will look for the next/previous model with a sort order. However you'll
likely want to have the various sort orders determined by a foreign key or some
other predicate. The easiest way (currently) is to override the method in
question.

