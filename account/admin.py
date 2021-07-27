from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    fieldsets=()
    filter_horizontal=()
    list_filter=()
    list_display=('email','username','login_date','is_active','is_admin')