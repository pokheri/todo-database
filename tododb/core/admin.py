from django.contrib import admin

# Register your models here.

from .models import Creater, RequestedOtp, Tasks


admin.site.register(RequestedOtp)
admin.site.register(Tasks)
admin.site.register(Creater)
