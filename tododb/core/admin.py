from django.contrib import admin

# Register your models here.

from .models import Creater, RequestedOtp


admin.site.register(RequestedOtp)

admin.site.register(Creater)
