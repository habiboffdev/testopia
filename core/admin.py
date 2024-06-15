from django.contrib import admin
from core import models
# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ["uid", "full_name"]
    list_display = ['username', 'full_name', 'rating', 'platform', 'step','is_active','is_superuser']
