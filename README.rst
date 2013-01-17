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

    class Book(Orderable):
        ...


Note: If your subclass of Orderable has a Metaclass then make sure it subclasses the Orderable one so the model is sorted by ``sort_order``.


Subclass the appropriate Orderable admin classes: ::

    class SomeInlineClass(OrderableTabularInline):
        ...

    class SomeAdminClass(OrderableAdmin):
        ...


You need jQuery 1.2+ and jQuery UI 1.5+ available in the Admin for the actual moveable UI. You can either override the base admin template or add them in a Media class: ::

    class SomeAdminClass(OrderableAdmin):
        class Media:
            js = (
                'path/to/jquery.js',
                'path/to/jquery.ui.js',
            )

