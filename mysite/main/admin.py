from django.contrib import admin
from .models import Customer
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.



class CustomerAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Title/date", {'fields': ["Customer_name", "Customer_published"]}),
        ("image location", {'fields': ["Customer_imageurl"]}),
        ("scrap url", {'fields': ["Customer_link"]}),
        ("Content", {"fields": ["Customer_content"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }


admin.site.register(Customer,CustomerAdmin)