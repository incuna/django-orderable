from django.contrib import admin

from orderable.admin import OrderableAdmin
from .models import Item


admin.site.register(Item, OrderableAdmin)
