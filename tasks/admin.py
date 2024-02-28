from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_tasks', 'undone_tasks', 'owner', 'recent_tasks']
    list_display_links = ['name']
    list_filter = ['owner']
    search_fields = ['name']
    fieldsets = (
        (None, {
            "fields": (
                'name', 'owner', #'youtube_video_hash',
            ),
        }),
    )
    autocomplete_fields = ['owner']

    def total_tasks(self, obj: models.Plan):
        return obj.tasks.count()
    total_tasks.short_description = _("total tasks")

    def undone_tasks(self, obj: models.Plan):
        return obj.tasks.filter(is_done=False).count()
    undone_tasks.short_description = _("undone tasks")

    def recent_tasks(self, obj: models.Plan):
        return "; ".join(obj.tasks.order_by('-created_at').values_list('name', flat=True)[:3])
    recent_tasks.short_description = _("recent tasks")



class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_done', 'deadline', 'plan', 'owner', 'created_at']
    list_filter = ['is_done', 'deadline', 'created_at']
    search_fields = ['name', 'description', 'plan__name',
                      'owner__last_name', 'owner__username']
    list_editable = ['is_done', 'owner', 'plan']
    readonly_fields = ['id', 'created_at', 'updated_at']
    autocomplete_fields = ['plan', 'owner']
    fieldsets = (
        (_("general").title(), {
            "fields": (
                ('name', 'deadline'),
                'description', 'is_done',
            ),
        }),
        (_("ownership").title(), {
            "fields": (
                ('owner', 'plan'),
            ),
        }),
        (_("temporal tracking").title(), {
            "fields": (
                ('created_at', 'updated_at', 'id'),
            ),
        }),
    )

admin.site.register(models.Plan)
admin.site.register(models.Task)
