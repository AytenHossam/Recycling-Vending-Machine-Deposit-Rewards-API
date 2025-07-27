from django.contrib import admin
from .models import Machine, Deposit, AdminProfile

admin.site.register(Machine)
admin.site.register(Deposit)
admin.site.register(AdminProfile)
