from django.contrib import admin
from .models import GovEmployee


# Register your models here.


class GovEmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'full_name')
    search_fields = ['emp_id', 'full_name']


admin.site.register(GovEmployee, GovEmployeeAdmin)

