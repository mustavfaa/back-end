from django.contrib import admin
from .models import LibraryUser, AccessToEdit, RoleHistory, PageCabinet
# Register your models here.

admin.site.register(RoleHistory)
# admin.site.register(PageCabinet)


@admin.register(AccessToEdit)
class AccessToEditAdmin(admin.ModelAdmin):
    autocomplete_fields = ['school']
    list_display = ['school', 'edit_status', 'status_12', 'school_id']
    search_fields = ['school__name_ru']
    list_filter = ['school__nash']
    list_editable = ['edit_status', 'status_12']


@admin.register(LibraryUser)
class LibraryUserAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user', 'create_school']
    search_fields = ['user']
    list_display = ['user']
