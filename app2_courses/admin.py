from django.contrib import admin

# Register your models here.
from .models import Standard, Subject, Lesson

admin.site.register( Standard)
admin.site.register( Subject)
admin.site.register( Lesson)
# , Subject, Lesson