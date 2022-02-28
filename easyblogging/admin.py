from django.contrib import admin
from .models import BlogModel,Category

# Register your models here.
admin.site.register(BlogModel)
admin.site.register(Category)