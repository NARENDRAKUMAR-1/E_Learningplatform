from django.contrib import admin

# Register your models here.
from .models import user_profile

admin.site.register( user_profile)
