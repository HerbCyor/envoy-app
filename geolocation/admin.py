from django.contrib import admin
from .models import FileRequest

# Register your models here.


class FileRequestAdmin(admin.ModelAdmin):
    list_display = ["user", "api_calls", "date", "input_file", "output_file"]


admin.site.register(FileRequest, FileRequestAdmin)
