from django.conf import settings

EDITABLE = getattr(settings, 'ORDERABLE_ORDER_EDITABLE', True)
