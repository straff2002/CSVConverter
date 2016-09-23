from django.contrib import admin

# Register your models here.

from .models import Configurations, ConvertedFiles

admin.site.register(Configurations)

admin.site.register(ConvertedFiles)
