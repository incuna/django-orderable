from django.db import models

class Orderable(models.Model):
    """An orderable object that keeps all the instances in an enforced order
    If there's a unique_together which includes the sort_order field then that
    will be used when checking for collisions etc.
    
    This  works well for inlines, which can be manually reordered by entering
    numbers, and the save function will prevent against collisions.
    
    For main objects, you would want to also use "OrderableAdmin", which will
    make a nice jquery admin interface.
    
    """
    
    sort_order = models.IntegerField(default=0,blank=True)
    
    class Meta:
        abstract = True
        ordering = ['sort_order']
        
    def get_unique_fields(self):
        """Fetches a list of field names that are set as unique with the sort order"""
        for unique_together in self._meta.unique_together:
            # for together in togethers:
            if 'sort_order' in unique_together:
                unique_fields = list(unique_together)
                unique_fields.remove('sort_order')
                return unique_fields
    
    
    def get_filters(self):
        """Builds a dictionary of kwargs that can be used to select unique together records"""
        unique_fields = self.get_unique_fields()
        if unique_fields:
            kwargs = {}
            for field in unique_fields:
                kwargs[field] = getattr(self, field)
            return kwargs

    def get_filtered_manager(self):
        """Returns the appropriate manager which may already have a filter applied based on the unique_together"""
        obj = type(self)
        extra_kwargs = self.get_filters()
        if extra_kwargs:
            return obj.objects.filter(**extra_kwargs)
        
        return obj.objects

    def next(self):
        objects = self.get_filtered_manager()
        
        try:
            next = objects.filter(sort_order__gt=self.sort_order).order_by('sort_order')[0]
            return next
        except IndexError:
            return None

    def prev(self):
        objects = self.get_filtered_manager()
        
        try:
            prev = objects.filter(sort_order__lt=self.sort_order).order_by('-sort_order')[0]
            return prev
        except IndexError:
            return None
        
    def save(self, *args, **kwargs):
        """All sorts of database-heavy jiggery-pokery which will keep the unique order in sync."""
        obj = type(self)
        objects = self.get_filtered_manager()
        
        if not self.sort_order:
            try:
                max_obj = objects.all().order_by('-sort_order')[0]
                self.sort_order = max_obj.sort_order + 1
            except IndexError:
                self.sort_order = 1
    
        # try and get any collisions
        try:
            collision = objects.exclude(pk=self.pk).get(sort_order=self.sort_order)
            to_shift_objs = objects.filter(sort_order__gte=self.sort_order).order_by('-sort_order')
            
            for to_shift in to_shift_objs:
                to_shift.sort_order += 1
                to_shift.save()
            
        except obj.DoesNotExist:
            #all good
            pass
    
        super(Orderable, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def sort_order_display(self):
        return "<span id='neworder-%s' class='sorthandle'>%s</span>" % (self.id, self.sort_order)
    sort_order_display.allow_tags = True
    sort_order_display.short_description = 'Order'
    sort_order_display.admin_order_field = 'sort_order'
  
# South rules - Not used?

# rules = [
#   (
#     (ImageWithThumbsField),
#     [],
#     {
#     },
#   )
# ]
# 
# 
# from south.modelsinspector import add_introspection_rules
# add_introspection_rules(rules, ["^incuna\.db\.models"])
