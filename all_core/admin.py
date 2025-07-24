from django.contrib import admin

# Register your models here.
from .models import RoutineModel, TaskModel, RoutineTotalModel, TotalModel
from .models import PassMarksModel, DetailsModel


class RoutineAdmin(admin.ModelAdmin):
    list_display = ('number', 'limited')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('routine', 'code', 'name')

class MarksAdmin(admin.ModelAdmin):
    list_display = ('date', 'task', 'bool_done', 'done', 'marks',)
    list_display_links = ['task']

class RouitineTotalAdmin(admin.ModelAdmin):
    list_display = ('routine', 'date' , 'rtotal')

class TotalAdmin(admin.ModelAdmin):
    list_display = ('date', 'total', 'passorfail')

admin.site.register(RoutineModel, RoutineAdmin)
admin.site.register(TaskModel, TaskAdmin)
admin.site.register(RoutineTotalModel, RouitineTotalAdmin)
admin.site.register(TotalModel, TotalAdmin)
admin.site.register(PassMarksModel)
admin.site.register(DetailsModel)