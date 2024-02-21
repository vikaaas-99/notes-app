from collections.abc import Sequence
from django.contrib import admin
from django.http import HttpRequest
from .models import *

# Register your models here.


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]


@admin.register(LogNoteHistory)
class LogNoteHistoryAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    

@admin.register(SharedNotes)
class SharedNotesAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]