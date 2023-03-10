from django.contrib import admin

from tracker_app.models import Issue
from tracker_app.models import Type
from tracker_app.models import Status
from tracker_app.models.projects import Project


# Register your models here.
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'summary', 'status', 'created_at')
    list_filter = ('status', 'id')
    search_fields = ('status', 'types', 'created_at')
    list_editable = ('summary', 'status')


admin.site.register(Issue, IssueAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Type, TypeAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Status, TypeAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_editable = ['name']


admin.site.register(Project, ProjectAdmin)
