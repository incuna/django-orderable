from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


csrf_protect_m = method_decorator(csrf_protect)


class OrderableAdmin(admin.ModelAdmin):
    """
    jQuery orderable objects in the admin.

    You'll want your object to subclass orderable.models.Orderable and you
    want to add sort_order_display to list_display.
    """
    list_display = ('__str__', 'sort_order_display')

    change_list_template = "admin/orderable_change_list.html"

    def get_urls(self):
        patterns = super(OrderableAdmin, self).get_urls()
        patterns.insert(
            # insert just before (.+) rule
            # (see django.contrib.admin.options.ModelAdmin.get_urls)
            -1,
            path(
                'reorder/',
                self.reorder_view,
                name=self.get_url_name()
            )
        )
        return patterns

    def get_url_name(self):
        meta = self.model._meta
        model_name = meta.model_name

        return '{0}admin_{1}_{2}_reorder'.format(
            self.admin_site.name, meta.app_label, model_name,
        )

    @csrf_protect_m
    def reorder_view(self, request):
        """The 'reorder' admin view for this model."""
        model = self.model

        if not self.has_change_permission(request):
            raise PermissionDenied

        if request.method == "POST":
            object_pks = request.POST.getlist('neworder[]')
            model.objects.set_orders(object_pks)

        return HttpResponse("OK")

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js',
        )


class OrderableTabularInline(admin.TabularInline):
    """
    jQuery orderable objects in the admin.

    You'll want your object to subclass orderable.models.Orderable.
    """
    template = "admin/edit_inline/orderable_tabular.html"

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js',
        )
