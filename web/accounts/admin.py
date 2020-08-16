from django.contrib import admin
from .models import *

class customeradmin(admin.ModelAdmin):
    class Meta:
        model=customer
    list_display=['name','phone','email']
    #list_display_links=['phone','email']
    #list_editable=['name']
    #search_fields=['name','email']
    #list_filter=['date_created']
admin.site.register(customer,customeradmin)
admin.site.register(product)
admin.site.register(order)
admin.site.register(tag)
# Register your models here.
