from django.contrib import admin

from .models import Entry, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner', 'date_added')
    list_filter = ('owner',)
    search_fields = ('text',)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('topic', 'date_added')
    list_filter = ('topic__owner',)
    search_fields = ('text',)
