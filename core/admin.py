from django.contrib import admin

from core.models import Channel, Content

# Register your models here.


class ContentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Content._meta.get_fields()]


admin.site.register(Content, ContentAdmin)


class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'language', 'picture', "sub_channel"]


admin.site.register(Channel, ChannelAdmin)
