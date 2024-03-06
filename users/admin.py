from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    list_display = ("username", "last_login", "date_joined", "is_active")
    list_display_links = ["username"]
    readonly_fields = ("last_login", "date_joined")
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(MyUser, MyUserAdmin)
