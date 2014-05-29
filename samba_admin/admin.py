from django.contrib import admin

from models import ShareConnection


class ShareConnectionAdmin(admin.ModelAdmin):
    list_display = ('letter', 'server', 'path')
    search_fields = ['path']
    filter_horizontal = ('groups', )

admin.site.register(ShareConnection, ShareConnectionAdmin)
