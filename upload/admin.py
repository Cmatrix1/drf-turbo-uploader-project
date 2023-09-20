from django.contrib import admin

from upload.models import FileModel


class FileModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'status', 'size', 'created_at')
    search_fields = ('filename',)
    list_filter = ('status', 'created_at')

admin.site.register(FileModel, FileModelAdmin)
