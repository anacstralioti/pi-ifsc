from django.contrib import admin

# Register your models here.
from .models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_admin')
    list_filter = ('is_admin',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

admin.site.register(Perfil, PerfilAdmin)
